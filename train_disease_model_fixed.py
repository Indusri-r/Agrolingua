import os
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ==========================================
# DATASET PATH
# ==========================================
DATASET_DIR = r"C:\Agrolinga\dataset final\agrolingua_synthetic_dataset"

TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
TEST_DIR = os.path.join(DATASET_DIR, "test")

# ==========================================
# SETTINGS
# ==========================================
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 15

MODEL_PATH = "models/disease_model.keras"
CLASS_MAPPING_PATH = "models/class_mapping.json"

# ==========================================
# CREATE MODELS FOLDER
# ==========================================
os.makedirs("models", exist_ok=True)

# ==========================================
# IMAGE AUGMENTATION
# ==========================================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3],
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(
    rescale=1./255
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

# ==========================================
# LOAD DATASETS
# ==========================================
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='sparse'
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='sparse'
)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='sparse',
    shuffle=False
)

# ==========================================
# CLASS NAMES
# ==========================================
class_names = list(train_generator.class_indices.keys())

print("\n========== DETECTED CLASSES ==========\n")

for cls in class_names:
    print(cls)

print("\n======================================")

# ==========================================
# PRETRAINED MOBILENETV2
# ==========================================
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

# ==========================================
# UNFREEZE MODEL
# ==========================================
base_model.trainable = True

# Freeze first layers only
for layer in base_model.layers[:100]:
    layer.trainable = False

# ==========================================
# BUILD FINAL MODEL
# ==========================================
model = keras.Sequential([

    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.4),

    layers.Dense(
        256,
        activation='relu'
    ),

    layers.Dropout(0.3),

    layers.Dense(
        len(class_names),
        activation='softmax'
    )

])

# ==========================================
# COMPILE MODEL
# ==========================================
model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=0.0001
    ),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================================
# MODEL SUMMARY
# ==========================================
model.summary()

# ==========================================
# CALLBACKS
# ==========================================
callbacks = [

    keras.callbacks.EarlyStopping(
        patience=5,
        restore_best_weights=True
    ),

    keras.callbacks.ReduceLROnPlateau(
        patience=3,
        factor=0.2
    ),

    keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        save_best_only=True
    )

]

# ==========================================
# CLASS WEIGHTS
# Helps reduce cotton bias
# ==========================================
class_weights = {}

for i in range(len(class_names)):
    class_weights[i] = 1.0

# ==========================================
# TRAIN MODEL
# ==========================================
print("\n========== TRAINING STARTED ==========\n")

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1
)

# ==========================================
# EVALUATE MODEL
# ==========================================
print("\n========== EVALUATING MODEL ==========\n")
 p
test_loss, test_accuracy = model.evaluate(
    test_generator
)

print(f"\nTest Accuracy: {test_accuracy:.4f}")

# ==========================================
# SAVE MODEL
# ==========================================
model.save(MODEL_PATH)

print(f"\nModel saved at:")
print(MODEL_PATH)

# ==========================================
# SAVE CLASS MAPPING
# ==========================================
class_mapping = {}

for class_name, index in train_generator.class_indices.items():

    class_mapping[str(index)] = class_name

with open(
    CLASS_MAPPING_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        class_mapping,
        f,
        indent=4
    )

print("\n========== CLASS MAPPING ==========\n")

print(json.dumps(
    class_mapping,
    indent=4
))

print("\n===================================")

print("\nTraining Completed Successfully!")