import os
import json
from pathlib import Path
import numpy as np

# TensorFlow imports
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from PIL import Image


IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10
SEED = 42

MODEL_SAVE_PATH = 'models/disease_model.keras'
CLASS_MAPPING_PATH = 'models/class_mapping.json'


def _is_image_file(p: Path) -> bool:
    return p.suffix.lower() in {'.jpg', '.jpeg', '.png'}


def _collect_labeled_images(root: Path):
    """Collect (image_path, label_str) pairs from PlantVillage-like directories.

    Supported structures in this repo:
      - root/train/<class_name>/*.jpg (if class folders exist)
      - root/train/*.<jpg> with accompanying .txt label files (if present)

    In your dataset, test/train images appear as:
      datasets/PlantDisease416x416/PlantDisease416x416/train/*.jpg
      datasets/PlantDisease416x416/PlantDisease416x416/test/*.jpg
      datasets/PlantDisease416x416/PlantDisease416x416/train/*.txt (may contain labels)

    If no class folders exist and txt labels are not in a parseable format,
    we fall back to treating each txt as the label of the image.

    Label conventions used when parsing:
      - If txt is empty => label='healthy'
      - If txt contains a single token => label=token
      - If txt contains multiple tokens => label=first token

    NOTE: If your txt files are bounding boxes (YOLO format), first token is class_id.
          In that case we map class_id strings to names via ids encountered.
    """
    train_dir = root / 'train'
    if not train_dir.exists():
        return []

    pairs = []

    # Case 1: class subfolders exist
    subdirs = [p for p in train_dir.iterdir() if p.is_dir()]
    if subdirs:
        class_names = sorted([d.name for d in subdirs])
        for cname in class_names:
            cdir = train_dir / cname
            for img_path in cdir.rglob('*'):
                if _is_image_file(img_path):
                    pairs.append((str(img_path), cname))
        return pairs

    # Case 2: flat folder with paired .txt labels
    # Collect images; attempt to parse label from sibling .txt
    for img_path in train_dir.iterdir():
        if not _is_image_file(img_path):
            continue
        txt_path = img_path.with_suffix('.txt')
        label = 'healthy'
        if txt_path.exists():
            try:
                txt = txt_path.read_text(encoding='utf-8', errors='ignore').strip()
                if txt:
                    first_token = txt.split()[0]
                    label = first_token
            except Exception:
                label = 'healthy'
        pairs.append((str(img_path), str(label)))

    return pairs


def _build_dataset(image_paths, labels, class_to_id):
    label_ids = np.array([class_to_id[l] for l in labels], dtype=np.int32)

    img_paths = np.array(image_paths)

    def _load_image(path):
        img_raw = tf.io.read_file(path)
        img = tf.image.decode_image(img_raw, channels=3, expand_animations=False)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = tf.image.resize(img, IMG_SIZE)
        return img

    ds = tf.data.Dataset.from_tensor_slices((img_paths, label_ids))

    def _map_fn(path, y):
        x = _load_image(path)
        return x, y

    ds = ds.map(_map_fn, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.shuffle(len(image_paths), seed=SEED, reshuffle_each_iteration=True)
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds


def build_model(num_classes: int):
    base_model = keras.applications.ResNet50(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False

    inputs = keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = keras.Model(inputs, outputs)

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Train plant disease classification model.')
    parser.add_argument(
        '--dataset-root',
        default=None,
        help='Root dataset path for PlantVillage-style structure (expects <root>/train/<label>/images)'
    )
    args = parser.parse_args()

    tf.random.set_seed(SEED)

    candidates = []
    if args.dataset_root:
        candidates.append(Path(args.dataset_root))

    repo_root = Path('.')
    # Keep existing candidates as fallback
    candidates.extend([
        repo_root / 'datasets/PlantDisease416x416/PlantDisease416x416',
        repo_root / 'datasets/PlantDiseases100x100/PlantDiseases100x100',
    ])


    all_pairs = []
    used_roots = []
    for r in candidates:
        if r.exists():
            pairs = _collect_labeled_images(r)
            if pairs:
                used_roots.append(str(r))
                all_pairs.extend(pairs)

    if not all_pairs:
        raise RuntimeError('No training images found. Check datasets/*/train directories.')

    image_paths = [p for p, _ in all_pairs]
    labels = [l for _, l in all_pairs]

    # Normalize labels
    labels = [str(l).strip() if str(l).strip() else 'healthy' for l in labels]

    unique_labels = sorted(list(set(labels)))
    class_to_id = {lab: i for i, lab in enumerate(unique_labels)}
    id_to_class = {i: lab for lab, i in class_to_id.items()}

    # Simple split
    rng = np.random.default_rng(SEED)
    idx = np.arange(len(image_paths))
    rng.shuffle(idx)
    split = int(0.8 * len(idx))
    train_idx, val_idx = idx[:split], idx[split:]

    train_paths = [image_paths[i] for i in train_idx]
    train_labels = [labels[i] for i in train_idx]
    val_paths = [image_paths[i] for i in val_idx]
    val_labels = [labels[i] for i in val_idx]

    train_ds = _build_dataset(train_paths, train_labels, class_to_id)
    val_ds = _build_dataset(val_paths, val_labels, class_to_id)

    model = build_model(num_classes=len(unique_labels))

    callbacks = [
        keras.callbacks.EarlyStopping(patience=4, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(patience=2, factor=0.3)
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )

    os.makedirs('models', exist_ok=True)

    # Save model artifacts.
    # Using .keras first is preferred by the inference code.
    model.save(MODEL_SAVE_PATH)

    # Backup save to ensure we have *some* loadable artifact even if one format fails.
    backup_h5_path = 'models/disease_model_backup.h5'
    try:
        model.save(backup_h5_path)
    except Exception:
        pass

    # Post-save verification
    saved_files = []
    for p in [MODEL_SAVE_PATH, backup_h5_path]:
        try:
            if Path(p).exists():
                saved_files.append(p)
        except Exception:
            pass

    print(f"Saved model files: {saved_files}")

    # Save mapping as expected by model_stub.py: mapping[str(id)] = class_name
    mapping = {str(i): id_to_class[i] for i in range(len(unique_labels))}
    with open(CLASS_MAPPING_PATH, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)

    print('==============================')
    print('Training complete')
    print('Used dataset roots:')
    for u in used_roots:
        print(' -', u)
    print('Num classes:', len(unique_labels))
    print('Classes:', unique_labels[:50], '...')
    if 'val_accuracy' in history.history:
        best_val_acc = max(history.history['val_accuracy'])
        print('Best val_accuracy:', best_val_acc)
    print('Saved:', MODEL_SAVE_PATH)
    print('Saved:', CLASS_MAPPING_PATH)


if __name__ == '__main__':
    main()

