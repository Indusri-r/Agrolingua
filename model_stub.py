from PIL import Image
import os
import cv2
import numpy as np
from pathlib import Path
from languages import get_translation

# =========================
# MODEL PATHS
# =========================
MODEL_PATH = 'models/disease_model.keras'
CLASS_MAPPING_PATH = 'models/class_mapping.json'

# =========================
# GLOBAL VARIABLES
# =========================
_disease_model = None
_class_names = []

# =========================
# LOAD MODEL
# =========================
def _load_disease_model():

    global _disease_model, _class_names

    if _disease_model is not None:
        return True

    try:

        import tensorflow as tf
        from tensorflow.keras.models import load_model
        import json

        # Load trained CNN model
        if os.path.exists(MODEL_PATH) and os.path.exists(CLASS_MAPPING_PATH):

            _disease_model = load_model(MODEL_PATH)

            print(f"Model loaded: {MODEL_PATH}")

            # Load class mapping
            with open(CLASS_MAPPING_PATH, 'r', encoding='utf-8') as f:
                mapping = json.load(f)

            mapping_keys = sorted(map(int, mapping.keys()))

            _class_names = [mapping[str(i)] for i in mapping_keys]

            print(f"Loaded {len(_class_names)} classes")

            return True

    except Exception as e:

        print("Model loading failed:", e)

    return False

# =========================
# CNN PREDICTION
# =========================
def predict_disease_nn(image_path):

    global _disease_model, _class_names

    from tensorflow.keras.preprocessing import image as kimage

    # =========================
    # LOAD IMAGE
    # =========================

    img = kimage.load_img(
        image_path,
        target_size=(224, 224)
    )

    # =========================
    # PREPROCESS IMAGE
    # =========================

    arr = kimage.img_to_array(img)

    arr = arr / 255.0

    arr = np.expand_dims(arr, 0)

    # =========================
    # MODEL PREDICTION
    # =========================

    preds = _disease_model.predict(
        arr,
        verbose=0
    )

    # =========================
    # GET BEST CLASS
    # =========================

    idx = int(np.argmax(preds[0]))

    confidence = float(preds[0][idx]) * 100

    # =========================
    # SAFE CLASS LOOKUP
    # =========================

    if idx < len(_class_names):

        disease_class = _class_names[idx]

    else:

        disease_class = "unknown_disease"

    # =========================
    # DEBUG OUTPUT
    # =========================

    print("\n========== MODEL PREDICTION ==========")

    print("Predicted Index:", idx)

    print("Predicted Class:", disease_class)

    print("Confidence:", confidence)

    print("======================================\n")

    return disease_class, confidence
# =========================
# =========================
def process_image(image_path, lang='en'):

    try:

        # =========================
        # LOAD MODEL
        # =========================

        if _load_disease_model():

            disease_class, confidence = predict_disease_nn(
                image_path
            )

            # =========================
            # HANDLE CLASS NAMES
            # =========================

            # Example:
            # Tomato___Late_blight

            if '___' in disease_class:

                parts = disease_class.split('___')

                plant_name = parts[0]

                disease_name = (
                    ' '.join(parts[1:])
                    .replace('_', ' ')
                    .title()
                )

            # Example:
            # rice_blast
            # wheat_rust

            else:

                parts = disease_class.split('_')

                # Plant name
                plant_name = parts[0].capitalize()

                # Disease name
                if len(parts) > 1:

                    disease_name = (
                        ' '.join(parts[1:])
                        .replace('_', ' ')
                        .title()
                    )

                else:

                    disease_name = "Healthy"

            return {

                'status': 'success',

                'plant_name': plant_name,

                'disease': disease_name,

                'confidence': confidence,

                'model_used': 'CNN Disease Model',

                'full_class': disease_class
            }

        # =========================
        # FALLBACK HEURISTIC
        # =========================

        cv_img = cv2.imread(image_path)

        if cv_img is None:

            return {
                'status': 'error',
                'message': 'Cannot load image'
            }

        pest_key = detect_pest_disease(cv_img)

        disease_text = get_translation(
            pest_key,
            lang
        )

        return {

            'status': 'fallback',

            'plant_name': 'Unknown',

            'disease': disease_text,

            'confidence': 65.0,

            'model_used': 'Heuristic Detection'
        }

    except Exception as e:

        return {

            'status': 'error',

            'message': str(e)
        }
# =========================
# SIMPLE HEURISTIC DETECTION
# =========================
def detect_pest_disease(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    height, width = image.shape[:2]

    total = height * width

    masks = {

        'rust': (
            np.array([15, 80, 80]),
            np.array([35, 255, 255])
        ),

        'blight': (
            np.array([0, 30, 30]),
            np.array([20, 200, 200])
        ),

        'mildew': (
            np.array([0, 0, 200]),
            np.array([180, 50, 255])
        )
    }

    for disease, (lower, upper) in masks.items():

        mask = cv2.inRange(hsv, lower, upper)

        ratio = cv2.countNonZero(mask) / total

        if ratio > 0.02:

            return disease

    return 'healthy'

# =========================
# DATASET INFO
# =========================
def get_dataset_statistics():

    return {

        'status': 'success',

        'dataset': 'Agrolingua Synthetic Dataset',

        'total_classes': len(_class_names),

        'classes': _class_names
    }

# =========================
# TEST
# =========================
if __name__ == '__main__':

    test_img = 'static/test_img.jpg'

    if os.path.exists(test_img):

        result = process_image(test_img)

        print(result)

    else:

        print("Test image not found")