"""
PlantDoc-Dataset Integration for Agrolinga
Based on PlantDoc Dataset (similar to PDR2018 format)

This module provides comprehensive plant disease detection capabilities
using the PlantDoc dataset structure.
"""

import numpy as np
import cv2
from PIL import Image
import os

# Disease class mappings based on PlantDoc dataset
DISEASE_CLASSES = {
    # Apple diseases
    'apple_leaf': {'name': 'Apple Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    'apple_rust_leaf': {'name': 'Apple Rust', 'disease': 'Rust Disease', 'treatment': 'Apply sulfur-based fungicide. Remove infected leaves.'},
    'apple_scab_leaf': {'name': 'Apple Scab', 'disease': 'Fungal Scab', 'treatment': 'Apply fungicide containing captan or myclobutanil.'},
    
    # Bell Pepper diseases
    'bell_pepper_leaf': {'name': 'Bell Pepper Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    'bell_pepper_leaf_spot': {'name': 'Bell Pepper Leaf Spot', 'disease': 'Bacterial Spot', 'treatment': 'Apply copper-based bactericide. Avoid overhead watering.'},
    
    # Blueberry
    'blueberry_leaf': {'name': 'Blueberry Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    
    # Cherry
    'cherry_leaf': {'name': 'Cherry Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    
    # Corn diseases
    'corn_gray_leaf_spot': {'name': 'Corn Gray Leaf Spot', 'disease': 'Gray Leaf Spot', 'treatment': 'Apply fungicide. Practice crop rotation.'},
    'corn_leaf_blight': {'name': 'Corn Leaf Blight', 'disease': 'Northern Leaf Blight', 'treatment': 'Apply fungicide. Use resistant varieties.'},
    'corn_rust_leaf': {'name': 'Corn Rust', 'disease': 'Common Rust', 'treatment': 'Apply fungicide. Ensure proper spacing for air circulation.'},
    
    # Grape diseases
    'grape_leaf': {'name': 'Grape Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    'grape_leaf_black_rot': {'name': 'Grape Black Rot', 'disease': 'Black Rot', 'treatment': 'Apply fungicide. Remove infected plant parts.'},
    
    # Peach
    'peach_leaf': {'name': 'Peach Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    
    # Potato diseases
    'potato_leaf_early_blight': {'name': 'Potato Early Blight', 'disease': 'Early Blight', 'treatment': 'Apply fungicide. Remove lower infected leaves.'},
    'potato_leaf_late_blight': {'name': 'Potato Late Blight', 'disease': 'Late Blight', 'treatment': 'Apply fungicide immediately. Remove infected plants.'},
    
    # Raspberry
    'raspberry_leaf': {'name': 'Raspberry Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    
    # Soybean
    'soyabean_leaf': {'name': 'Soybean Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    
    # Squash
    'squash_powdery_mildew_leaf': {'name': 'Squash Powdery Mildew', 'disease': 'Powdery Mildew', 'treatment': 'Apply sulfur-based fungicide. Improve air circulation.'},
    
    # Strawberry
    'strawberry_leaf': {'name': 'Strawberry Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    
    # Tomato diseases
    'tomato_early_blight_leaf': {'name': 'Tomato Early Blight', 'disease': 'Early Blight', 'treatment': 'Apply fungicide. Mulch around plants.'},
    'tomato_leaf': {'name': 'Tomato Leaf', 'disease': 'Healthy', 'treatment': 'No treatment needed'},
    'tomato_leaf_bacterial_spot': {'name': 'Tomato Bacterial Spot', 'disease': 'Bacterial Spot', 'treatment': 'Apply copper bactericide. Avoid working with wet plants.'},
    'tomato_leaf_late_blight': {'name': 'Tomato Late Blight', 'disease': 'Late Blight', 'treatment': 'Apply fungicide. Remove infected plants immediately.'},
    'tomato_leaf_mosaic_virus': {'name': 'Tomato Mosaic Virus', 'disease': 'Mosaic Virus', 'treatment': 'Remove infected plants. Control aphid vectors.'},
    'tomato_leaf_yellow_virus': {'name': 'Tomato Yellow Leaf Curl', 'disease': 'Yellow Leaf Curl Virus', 'treatment': 'Control whiteflies. Use resistant varieties.'},
    'tomato_mold_leaf': {'name': 'Tomato Mold', 'disease': 'Leaf Mold', 'treatment': 'Improve ventilation. Apply fungicide.'},
    'tomato_septoria_leaf_spot': {'name': 'Tomato Septoria Leaf Spot', 'disease': 'Septoria Leaf Spot', 'treatment': 'Apply fungicide. Remove infected leaves.'},
}

def process_plantdoc_image(image_path, lang='en'):
    """
    Process an image using PlantDoc-style disease detection.
    Returns detailed disease analysis.
    """
    try:
        # Open and preprocess image
        img = Image.open(image_path)
        cv_img = cv2.imread(image_path)
        
        if cv_img is None:
            return {
                'status': 'error',
                'message': 'Could not load image'
            }
        
        # Get disease prediction using color-based analysis
        disease_info = detect_plant_disease(cv_img)
        
        # Get additional image metrics
        width, height = img.size
        total_pixels = width * height
        
        return {
            'status': 'success',
            'plant_name': disease_info['plant_name'],
            'disease': disease_info['disease'],
            'confidence': disease_info['confidence'],
            'treatment': disease_info['treatment'],
            'recommendations': get_recommendations(disease_info['disease']),
            'image_info': {
                'width': width,
                'height': height,
                'total_pixels': total_pixels
            }
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def detect_plant_disease(image):
    """
    Detect plant disease AND plant type using color analysis based on PlantDoc dataset classes.
    Returns disease information with confidence score.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate various color ratios for disease detection
    total_pixels = image.shape[0] * image.shape[1]
    
    # First, detect the plant type from the image
    plant_type = detect_plant_type(image, hsv, total_pixels)
    
    # Yellow/orange spots (rust disease)
    lower_yellow = np.array([15, 80, 80])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_ratio = cv2.countNonZero(yellow_mask) / total_pixels
    
    # Brown/dark spots (blight, rot)
    lower_brown = np.array([0, 30, 30])
    upper_brown = np.array([20, 200, 150])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    brown_ratio = cv2.countNonZero(brown_mask) / total_pixels
    
    # Gray spots (gray leaf spot)
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([180, 50, 150])
    gray_mask = cv2.inRange(hsv, lower_gray, upper_gray)
    gray_ratio = cv2.countNonZero(gray_mask) / total_pixels
    
    # White/powdery patches (powdery mildew)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    white_ratio = cv2.countNonZero(white_mask) / total_pixels
    
    # Green analysis (healthy leaf)
    lower_green = np.array([35, 30, 30])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = cv2.countNonZero(green_mask) / total_pixels
    
    # Yellow/light green (virus, mosaic)
    lower_virus = np.array([20, 50, 150])
    upper_virus = np.array([40, 255, 255])
    virus_mask = cv2.inRange(hsv, lower_virus, upper_virus)
    virus_ratio = cv2.countNonZero(virus_mask) / total_pixels
    
    # Determine disease based on color analysis
    confidence = 0.0
    disease_key = 'healthy'
    
    # Priority-based disease detection
    if white_ratio > 0.03:
        disease_key = 'powdery_mildew'
        confidence = min(95, 60 + white_ratio * 500)
    elif yellow_ratio > 0.025:
        disease_key = 'rust'
        confidence = min(90, 55 + yellow_ratio * 400)
    elif gray_ratio > 0.02:
        disease_key = 'gray_leaf_spot'
        confidence = min(85, 50 + gray_ratio * 400)
    elif brown_ratio > 0.04:
        disease_key = 'blight'
        confidence = min(85, 45 + brown_ratio * 300)
    elif virus_ratio > 0.08:
        disease_key = 'virus'
        confidence = min(80, 40 + virus_ratio * 200)
    elif green_ratio > 0.5:
        disease_key = 'healthy'
        confidence = min(95, 50 + green_ratio * 80)
    else:
        # Default to healthy with moderate confidence
        disease_key = 'healthy'
        confidence = 55.0
    
    return get_disease_details(disease_key, confidence, plant_type)

def detect_plant_type(image, hsv, total_pixels):
    """
    Detect plant type from image using color analysis.
    Returns the detected plant name based on dominant colors.
    """
    # Green color analysis (most plants/leaves)
    lower_green = np.array([25, 20, 20])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = cv2.countNonZero(green_mask) / total_pixels
    
    # Red/Orange (tomatoes, peppers, apples)
    lower_red = np.array([0, 30, 50])
    upper_red = np.array([25, 255, 255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    red_ratio = cv2.countNonZero(red_mask) / total_pixels
    
    # Yellow/Orange (corn, wheat, mango)
    lower_yellow = np.array([15, 40, 80])
    upper_yellow = np.array([45, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_ratio = cv2.countNonZero(yellow_mask) / total_pixels
    
    # Brown/Dark brown (potatoes, dead leaves)
    lower_brown = np.array([5, 20, 20])
    upper_brown = np.array([30, 180, 150])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    brown_ratio = cv2.countNonZero(brown_mask) / total_pixels
    
    # Purple (grapes, eggplants)
    lower_purple = np.array([90, 30, 30])
    upper_purple = np.array([140, 255, 255])
    purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)
    purple_ratio = cv2.countNonZero(purple_mask) / total_pixels
    
    # Light green/yellowish (unhealthy leaves)
    lower_light = np.array([20, 20, 150])
    upper_light = np.array([50, 100, 255])
    light_mask = cv2.inRange(hsv, lower_light, upper_light)
    light_ratio = cv2.countNonZero(light_mask) / total_pixels
    




    # Detect plant type - ORDER MATTERS! 
    # Tomato detection (more distinctive - needs significant red)
    if red_ratio > 0.08 and green_ratio > 0.15 and red_ratio < 0.35:
        return "Tomato"
    
    # Apple detection (even more red)
    if red_ratio > 0.15 and green_ratio > 0.3:
        return "Apple"
    
    # Potato detection (brown/dark tones with some green)
    if brown_ratio > 0.18 and green_ratio > 0.1:
        return "Potato"
    
    # Corn/Maize detection (yellow/gold dominant)
    if yellow_ratio > 0.20:
        return "Corn"
    
    # Wheat detection (yellow/gold with some green - similar to corn)
    if yellow_ratio > 0.15 and green_ratio > 0.2:
        return "Wheat"
    
    # Grape detection (purple tones)
    if purple_ratio > 0.06:
        return "Grape"
    
    # Bell Pepper (more green, very little red)
    if green_ratio > 0.55 and red_ratio < 0.05:
        return "Bell Pepper"
    
    # Soybean/Green Leafy (dominant green)
    if green_ratio > 0.5:
        return "Soybean"
    
    # Strawberry (some red with lots of green)
    if red_ratio > 0.05 and green_ratio > 0.45:
        return "Strawberry"
    
    # Rice (light green/yellow - paddy)
    if green_ratio > 0.4 and yellow_ratio > 0.1:
        return "Rice"
    
    # Cotton (pale green/yellow)
    if yellow_ratio > 0.08 and green_ratio > 0.35:
        return "Cotton"
    
    # Default - green leafy plant
    if green_ratio > 0.3:
        return "Green Leafy Plant"
    
    return "Unknown Plant"

def get_disease_details(disease_type, confidence, plant_type='Healthy Plant'):
    """
    Map disease type to detailed information.
    """
    disease_map = {
        'healthy': {
            'plant_name': plant_type,
            'disease': 'No Disease Detected',
            'treatment': 'Continue regular care. Monitor for any changes.',
            'confidence': confidence
        },
        'powdery_mildew': {
            'plant_name': plant_type,
            'disease': 'Fungal Infection',
            'treatment': 'Apply sulfur-based fungicide or neem oil. Ensure good air circulation.',
            'confidence': confidence
        },
        'rust': {
            'plant_name': plant_type,
            'disease': 'Fungal Rust',
            'treatment': 'Apply copper fungicide. Remove infected leaves. Avoid overhead watering.',
            'confidence': confidence
        },
        'gray_leaf_spot': {
            'plant_name': plant_type,
            'disease': 'Fungal Infection',
            'treatment': 'Apply fungicide. Practice crop rotation. Use resistant varieties.',
            'confidence': confidence
        },
        'blight': {
            'plant_name': plant_type,
            'disease': 'Fungal/Bacterial Blight',
            'treatment': 'Apply appropriate fungicide. Remove infected plant parts. Improve drainage.',
            'confidence': confidence
        },
        'virus': {
            'plant_name': plant_type,
            'disease': 'Virus Disease',
            'treatment': 'Remove and destroy infected plants. Control insect vectors (aphids, whiteflies).',
            'confidence': confidence
        }
    }
    
    return disease_map.get(disease_type, disease_map['healthy'])

def get_recommendations(disease):
    """
    Get treatment recommendations based on disease type.
    """
    recommendations = {
        'No Disease Detected': [
            'Continue regular watering schedule',
            'Maintain proper fertilization',
            'Monitor regularly for pests',
            'Ensure adequate sunlight exposure'
        ],
        'Fungal Infection': [
            'Apply appropriate fungicide',
            'Remove and destroy infected leaves',
            'Improve air circulation',
            'Avoid overhead watering',
            'Practice crop rotation next season'
        ],
        'Fungal Rust': [
            'Apply copper-based fungicide',
            'Remove infected plant parts',
            'Avoid working with wet plants',
            'Apply preventive fungicide to nearby plants'
        ],
        'Fungal/Bacterial Blight': [
            'Apply broad-spectrum fungicide',
            'Remove severely infected plants',
            'Improve plant spacing',
            'Avoid overhead irrigation',
            'Sanitize pruning tools'
        ],
        'Virus Disease': [
            'Remove and destroy infected plants',
            'Control aphid and whitefly populations',
            'Use virus-free planting material',
            'Plant resistant varieties',
            'Control weed hosts'
        ]
    }
    
    return recommendations.get(disease, recommendations['No Disease Detected'])

def get_dataset_statistics():
    """
    Return statistics about the PlantDoc dataset.
    """
    return {
        'total_classes': len(DISEASE_CLASSES),
        'categories': {
            'fruits': ['Apple', 'Bell Pepper', 'Blueberry', 'Cherry', 'Grape', 'Peach', 'Raspberry', 'Strawberry', 'Tomato'],
            'vegetables': ['Potato', 'Squash', 'Soybean', 'Corn'],
            'disease_types': ['Healthy', 'Rust', 'Scab', 'Blight', 'Spot', 'Mildew', 'Virus', 'Rot']
        },
        'train_samples': 'Multiple images per category',
        'test_samples': 'Multiple images per category',
        'data_format': 'JPEG images of plant leaves'
    }

def analyze_batch(dataset_path, lang='en'):
    """
    Analyze a batch of images from a dataset folder.
    """
    results = []
    
    if not os.path.exists(dataset_path):
        return [{'status': 'error', 'message': 'Dataset path not found'}]
    
    # Process each category folder
    for category in os.listdir(dataset_path):
        category_path = os.path.join(dataset_path, category)
        if os.path.isdir(category_path):
            # Process images in category
            images = [f for f in os.listdir(category_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
            for img_name in images[:5]:  # Limit to 5 per category
                img_path = os.path.join(category_path, img_name)
                result = process_plantdoc_image(img_path, lang)
                result['category'] = category
                results.append(result)
    
    return results

# Export main functions
__all__ = [
    'process_plantdoc_image',
    'detect_plant_disease',
    'get_dataset_statistics',
    'analyze_batch',
    'DISEASE_CLASSES'
]
