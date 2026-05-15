import argparse
import os
import sys
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import zipfile

# Force UTF-8 output on Windows consoles to prevent progress bar encoding errors
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

MODEL_SAVE_PATH = 'models/disease_model.h5'
CLASS_MAPPING_PATH = 'models/class_mapping.json'
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5


def get_dataset_dir(dataset_root=None):
    print("Checking crop disease dataset...")
    candidates = []
    if dataset_root:
        candidates.append(Path(dataset_root))
    candidates.extend([
        Path("datasets/CropsDisease/Final_Dataset"),
        Path("datasets/crops-disease-dataset/Final_Dataset"),
        Path("dataset/CropsDisease/Final_Dataset"),
        Path("dataset/crops-disease-dataset/Final_Dataset"),
        Path("datasets/CropsDisease"),
        Path("datasets/crops-disease-dataset"),
        Path("dataset/CropsDisease"),
        Path("dataset/crops-disease-dataset"),
    ])

    if Path("datasets/crops_disease.zip").exists():
        try:
            print("Extracting datasets/crops_disease.zip...")
            with zipfile.ZipFile("datasets/crops_disease.zip", "r") as zip_ref:
                zip_ref.extractall("datasets/")
            print("Extraction complete.")
        except Exception as e:
            print("Failed to extract zip:", e)

    if Path("datasets/crops-disease.zip").exists():
        try:
            print("Extracting datasets/crops-disease.zip...")
            with zipfile.ZipFile("datasets/crops-disease.zip", "r") as zip_ref:
                zip_ref.extractall("datasets/")
            print("Extraction complete.")
        except Exception as e:
            print("Failed to extract zip:", e)

    for base_path in candidates:
        if not base_path.exists():
            continue

        if base_path.is_dir() and any(base_path.iterdir()):
            print("Using dataset directory:", base_path)
            return base_path

    print("No crop disease dataset found in expected locations.")
    print("Searched paths:")
    for p in candidates:
        print(" -", p)
    return None

def create_data_generators(dataset_dir, batch_size=BATCH_SIZE):
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    train_gen = datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=batch_size,
        class_mode="sparse",
        subset="training"
    )
    
    val_gen = datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=batch_size,
        class_mode="sparse",
        subset="validation"
    )
    
    class_names = list(train_gen.class_indices.keys())
    print("Dataset:", train_gen.samples, "train,", val_gen.samples, "val,", len(class_names), "classes")
    return train_gen, val_gen, class_names

def build_model(num_classes, weights=None):
    base_model = keras.applications.ResNet50(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=weights
    )
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(num_classes, activation="softmax")
    ])
    
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

def main():
    parser = argparse.ArgumentParser(description='Train a crop disease classification model.')
    parser.add_argument('--dataset', default=None, help='Root dataset path to the extracted crop disease dataset')
    parser.add_argument('--epochs', type=int, default=EPOCHS, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE, help='Training batch size')
    parser.add_argument('--steps-per-epoch', type=int, default=None, help='Override steps per epoch for faster training')
    parser.add_argument('--validation-steps', type=int, default=None, help='Override validation steps for faster training')
    parser.add_argument('--imagenet', action='store_true', help='Use ImageNet pretrained weights for ResNet50')
    args = parser.parse_args()

    dataset_dir = get_dataset_dir(args.dataset)
    if not dataset_dir:
        print("Dataset preparation failed. Provide a valid crop disease dataset path or extract datasets/crops_disease.zip or datasets/crops-disease.zip")
        return

    train_gen, val_gen, class_names = create_data_generators(dataset_dir, batch_size=args.batch_size)
    weights = 'imagenet' if args.imagenet else None
    if args.imagenet:
        print('Using ImageNet pretrained weights for ResNet50.')
    else:
        print('Training from scratch with random initialization.')
    model = build_model(len(class_names), weights=weights)

    steps_per_epoch = args.steps_per_epoch if args.steps_per_epoch is not None else max(1, train_gen.samples // args.batch_size)
    validation_steps = args.validation_steps if args.validation_steps is not None else max(1, val_gen.samples // args.batch_size)

    history = model.fit(
        train_gen,
        steps_per_epoch=steps_per_epoch,
        validation_data=val_gen,
        validation_steps=validation_steps,
        epochs=args.epochs,
        verbose=1
    )

    os.makedirs("models", exist_ok=True)
    model.save(MODEL_SAVE_PATH)

    mapping = {str(i): class_names[i] for i in range(len(class_names))}
    with open(CLASS_MAPPING_PATH, "w") as f:
        json.dump(mapping, f)

    print("Model saved to:", MODEL_SAVE_PATH)
    print("Class mapping saved to:", CLASS_MAPPING_PATH)
    print("Test with: python -c 'from model_stub import process_image; print(process_image(\"static/test_img.jpg\"))'")

if __name__ == "__main__":
    main()

