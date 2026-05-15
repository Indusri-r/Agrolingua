import os
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import zipfile

# Configuration
MODEL_SAVE_PATH = 'models/disease_model.h5'
CLASS_MAPPING_PATH = 'models/class_mapping.json'
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10  # Reduced for testing

def get_dataset_dir(dataset_root=None):
    """
    Auto-detect the crop disease dataset directory.
    Supports Kaggle-style extracted structures such as:
      datasets/CropsDisease/Final_Dataset
      datasets/crops-disease-dataset/Final_Dataset
    """
    print('Checking crop disease dataset...')
    candidate_roots = []
    if dataset_root:
        candidate_roots.append(Path(dataset_root))

    candidate_roots.extend([
        Path('datasets/CropsDisease/Final_Dataset'),
        Path('datasets/crops-disease-dataset/Final_Dataset'),
        Path('dataset/CropsDisease/Final_Dataset'),
        Path('dataset/crops-disease-dataset/Final_Dataset'),
        Path('datasets/CropsDisease'),
        Path('datasets/crops-disease-dataset'),
        Path('dataset/CropsDisease'),
        Path('dataset/crops-disease-dataset'),
    ])

    if Path('datasets/crops_disease.zip').exists():
        try:
            print('Extracting datasets/crops_disease.zip...')
            with zipfile.ZipFile('datasets/crops_disease.zip', 'r') as zip_ref:
                zip_ref.extractall('datasets/')
            print('Extraction complete.')
        except Exception as e:
            print('Failed to extract zip:', e)

    if Path('datasets/crops-disease.zip').exists():
        try:
            print('Extracting datasets/crops-disease.zip...')
            with zipfile.ZipFile('datasets/crops-disease.zip', 'r') as zip_ref:
                zip_ref.extractall('datasets/')
            print('Extraction complete.')
        except Exception as e:
            print('Failed to extract zip:', e)

    for base_path in candidate_roots:
        if not base_path.exists():
            continue

        if base_path.is_dir() and any(base_path.iterdir()):
            print(f'Using dataset directory: {base_path}')
            return base_path

    print('No valid crop disease dataset found. Checked:')
    for root in candidate_roots:
        print(' -', root)
    raise ValueError('Crop disease dataset not found. Place the extracted dataset under datasets/CropsDisease/Final_Dataset or provide --dataset path.')

def create_data_generators(dataset_dir):
    """
    Create memory-efficient generators.
    """
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )
    
    train_gen = datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='training',
        shuffle=True
    )
    
    val_gen = datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='validation',
        shuffle=False
    )
    
    class_names = list(train_gen.class_indices.keys())
    print(f'✅ Dataset ready: {train_gen.samples} train, {val_gen.samples} val, {len(class_names)} classes')
    
    return train_gen, val_gen, class_names

def build_crop_disease_model(num_classes):
    """
    ResNet50 transfer learning for crop disease classification.
    """
    base_model = keras.applications.ResNet50(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model():
    """
    Complete training pipeline.
    """
    dataset_dir = get_dataset_dir()
    train_gen, val_gen, class_names = create_data_generators(dataset_dir)
    
    model = build_crop_disease_model(len(class_names))
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.2, patience=3)
    ]
    
    history = model.fit(
        train_gen,
        steps_per_epoch=max(1, train_gen.samples // BATCH_SIZE),
        validation_data=val_gen,
        validation_steps=max(1, val_gen.samples // BATCH_SIZE),
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save
    os.makedirs('models', exist_ok=True)
    model.save(MODEL_SAVE_PATH)
    
    # Class mapping
    mapping = {str(i): name for i, name in enumerate(class_names)}
    with open(CLASS_MAPPING_PATH, 'w') as f:
        json.dump(mapping, f)
    
    print(f'✅ Model trained and saved!')
    print(f'Accuracy history: {max(history.history["val_accuracy"]):.3f}')
    print(f'Files: {MODEL_SAVE_PATH}, {CLASS_MAPPING_PATH}')
    print('\\nTest with: python -c \"from model_stub import process_image; print(process_image(\\"static/test_img.jpg\\"))\"')
    
    return model, class_names

if __name__ == '__main__':
    train_model()
