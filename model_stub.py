from PIL import Image
import os
import cv2
import numpy as np
from pathlib import Path
from languages import get_translation

# Crop disease model paths
MODEL_PATH = 'models/disease_model.h5'
CLASS_MAPPING_PATH = 'models/class_mapping.json'

# Global model variables
_disease_model = None
_class_names = []

def _load_disease_model():
    "Load the crop disease classification model if available."
    global _disease_model, _class_names
    if _disease_model is not None:
        return True

    try:
        import tensorflow as tf
        from tensorflow.keras.models import load_model
        import json

        if os.path.exists(MODEL_PATH) and os.path.exists(CLASS_MAPPING_PATH):
            _disease_model = load_model(MODEL_PATH)
            with open(CLASS_MAPPING_PATH, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            _class_names = [mapping[str(i)] for i in sorted(map(int, mapping.keys()))]
            print("Crop disease model loaded: %d params, %d classes" % (_disease_model.count_params(), len(_class_names)))
            return True
    except Exception as e:
        print("Model load failed:", e)

    print("Using heuristic fallback (train model first)")
    return False

def predict_disease_nn(image_path):
    "Deep learning prediction with the crop disease model."
    global _disease_model, _class_names
    from tensorflow.keras.preprocessing import image as kimage
    img = kimage.load_img(image_path, target_size=(224, 224))
    arr = kimage.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, 0)


    # Some saved models may expect multiple inputs. Try the common single-input path first.
    try:
        preds = _disease_model.predict(arr, verbose=0)
    except Exception:
        # Fallback: duplicate the same tensor for every model input.
        if hasattr(_disease_model, 'inputs') and _disease_model.inputs:
            preds = _disease_model.predict([arr] * len(_disease_model.inputs), verbose=0)
        else:
            raise
    idx = np.argmax(preds[0])
    conf = float(preds[0][idx])
    return _class_names[idx], conf

def process_image(image_path, lang='en'):
    "Production-ready prediction for app.py."
    try:
        if _load_disease_model():
            disease_class, confidence = predict_disease_nn(image_path)
            if '___' in disease_class:
                parts = disease_class.split('___')
                plant_name = parts[0]
                disease_name = ' '.join(parts[1:]).replace('_', ' ')
            else:
                plant_name = 'Unknown Plant'
                disease_name = disease_class
            if confidence < 0.1:
                confidence = confidence * 100  # Scale very low confidence (early training)

            return {
                'status': 'success',
                'plant_name': plant_name,
                'disease': 'healthy' if 'healthy' in disease_name.lower() else disease_name,
                'confidence': confidence,
                'model_used': 'Crop disease model',
                'full_class': disease_class
            }

        # Improved heuristic fallback
        cv_img = cv2.imread(image_path)
        if cv_img is None:
            return {'status': 'error', 'message': 'Cannot load image'}

        pest_key = detect_pest_disease(cv_img)
        disease_text = get_translation(pest_key, lang)

        return {
            'status': 'fallback',
            'plant_name': 'Unknown',
            'disease': disease_text,
            'confidence': 0.65,
            'model_used': 'Heuristics'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def detect_pest_disease(image):
    "Color heuristic detection."
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width = image.shape[:2]
    total = height * width

    masks = {
        'rust': (np.array([15,80,80]), np.array([35,255,255])),
        'blight': (np.array([0,30,30]), np.array([20,200,200])),
        'mildew': (np.array([0,0,200]), np.array([180,50,255]))
    }

    for disease, (lower, upper) in masks.items():
        mask = cv2.inRange(hsv, lower, upper)
        ratio = cv2.countNonZero(mask) / total
        if ratio > 0.02:
            return disease.replace('_', ' ')

    return 'healthy'


def get_dataset_dir():
    """Locate the configured crop disease dataset."""
    candidates = [
        Path('datasets/CropsDisease/Final_Dataset'),
        Path('datasets/crops-disease-dataset/Final_Dataset'),
        Path('dataset/CropsDisease/Final_Dataset'),
        Path('dataset/crops-disease-dataset/Final_Dataset'),
        Path('datasets/CropsDisease'),
        Path('datasets/crops-disease-dataset'),
        Path('dataset/CropsDisease'),
        Path('dataset/crops-disease-dataset'),
    ]
    for path in candidates:
        if path.exists() and path.is_dir() and any(path.iterdir()):
            return path
    return None


def get_dataset_statistics():
    """Return basic statistics about the crop disease dataset."""
    dataset_dir = get_dataset_dir()
    if dataset_dir is None:
        return {
            'status': 'missing_dataset',
            'message': 'Crop disease dataset not found.',
            'searched_paths': [str(p) for p in [
                Path('datasets/CropsDisease/Final_Dataset'),
                Path('datasets/crops-disease-dataset/Final_Dataset'),
                Path('dataset/CropsDisease/Final_Dataset'),
                Path('dataset/crops-disease-dataset/Final_Dataset')
            ]]
        }

    class_dirs = [p.name for p in dataset_dir.iterdir() if p.is_dir()]
    crop_groups = {}
    for class_name in class_dirs:
        if '___' in class_name:
            crop, disease = class_name.split('___', 1)
            crop_groups.setdefault(crop, []).append(disease)
        else:
            crop_groups.setdefault('Unknown', []).append(class_name)

    return {
        'status': 'success',
        'dataset_path': str(dataset_dir),
        'total_classes': len(class_dirs),
        'crops': sorted(crop_groups.keys()),
        'classes_by_crop': {crop: sorted(diseases) for crop, diseases in crop_groups.items()}
    }

if __name__ == '__main__':
    # Test
    test_img = 'static/test_img.jpg'
    if os.path.exists(test_img):
        print("Testing prediction:", process_image(test_img))
    else:
        print("Test image not found")

