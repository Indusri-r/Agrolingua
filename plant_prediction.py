import numpy as np


def predict_plant_type(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2):
    """
    Predict the type of plant to be grown based on sensor data.
    Uses comprehensive rule-based logic based on agricultural best practices.
    """
    recommendations = []
    
    # Rice prediction - requires high moisture, warm temperature
    if soil_moisture > 60 and temperature > 20 and temperature < 35 and ph_level > 5.5 and ph_level < 7.0:
        if npk_n > 40:
            recommendations.append("Rice (బ్రౌ) - Ideal for lowland flooded conditions. Requires standing water.")
    
    # Wheat prediction - moderate moisture, cool climate
    if 40 <= soil_moisture <= 70 and 15 <= temperature <= 25 and ph_level > 6.0 and ph_level < 7.5:
        if npk_n > 30 and npk_p > 15:
            recommendations.append("Wheat (గోధుమ) - Suitable for rabi season. Needs cool climate.")
    
    # Cotton prediction - drought tolerant, requires warm climate
    if soil_moisture < 50 and temperature > 25 and temperature < 40 and ph_level > 5.5 and ph_level < 8.0:
        recommendations.append("Cotton (पट्टु) - Drought tolerant crop. Requires warm climate.")
    
    # Maize prediction - moderate moisture, warm climate
    if 30 <= soil_moisture <= 60 and 20 <= temperature <= 35 and ph_level > 5.5 and ph_level < 7.5:
        if npk_n > 20:
            recommendations.append("Maize (मक्का) - Kharif crop. Requires moderate water.")
    
    # Groundnut prediction - well-drained soil, warm climate
    if 30 <= soil_moisture <= 50 and temperature > 20 and temperature < 35 and ph_level > 5.0 and ph_level < 7.0:
        if npk_p > 15 and npk_k > 20:
            recommendations.append("Groundnut (శెనగ) - Requires well-drained soil. Good for oil production.")
    
    # Sugarcane prediction - high moisture, tropical
    if soil_moisture > 70 and temperature > 25 and temperature < 40 and ph_level > 6.0 and ph_level < 7.5:
        recommendations.append("Sugarcane ( చక్కర) - Requires high moisture. Long duration crop.")
    
    # Mustard prediction - low moisture, cool climate
    if soil_moisture < 40 and 15 <= temperature <= 25 and ph_level > 6.0 and ph_level < 7.5:
        recommendations.append("Mustard (एలసి) - Rabi crop. Low water requirement.")
    
    # Onion prediction - moderate moisture
    if 30 <= soil_moisture <= 50 and 15 <= temperature <= 30 and ph_level > 6.0 and ph_level < 7.5:
        recommendations.append("Onion (ఉల్లిపాయ) - Requires moderate water. Short duration crop.")
    
    # If no specific recommendation, provide general crop advice
    if not recommendations:
        if soil_moisture > 60:
            recommendations.append("Paddy/Rice - Suitable for high moisture conditions")
        elif soil_moisture < 30:
            recommendations.append("Millets (Jowar/Bajra) - Drought resistant crops")
        else:
            recommendations.append("General Vegetables - Suitable for moderate conditions")
    
    # Add soil health analysis
    soil_health = []
    if ph_level < 5.5:
        soil_health.append("⚠️ Soil is highly acidic - add lime")
    elif ph_level > 8.0:
        soil_health.append("⚠️ Soil is highly alkaline - add sulfur")
    else:
        soil_health.append("✅ Soil pH is optimal")
    
    if npk_n < 20:
        soil_health.append("⚠️ Nitrogen is low - add nitrogen fertilizer")
    if npk_p < 10:
        soil_health.append("⚠️ Phosphorus is low - add phosphorus fertilizer")
    if npk_k < 15:
        soil_health.append("⚠️ Potassium is low - add potassium fertilizer")
    
    if npk_n > 40 and npk_p > 20 and npk_k > 30:
        soil_health.append("✅ NPK levels are good")
    
    return "\n".join(recommendations) + "\n\n" + "\n".join(soil_health)

def predict_plant(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2):
    """
    Predict the BEST single crop based on sensor data.
    Returns only ONE crop recommendation, not multiple.
    Uses scoring algorithm to find best match.
    """
    
    # Define crop requirements as a scoring system
    crops = {
        'Rice': {
            'moisture': (60, 100),
            'temperature': (20, 35),
            'ph': (5.5, 7.0),
            'npk_n': (40, 200),
            'priority': 1
        },
        'Wheat': {
            'moisture': (40, 70),
            'temperature': (15, 25),
            'ph': (6.0, 7.5),
            'npk_n': (30, 100),
            'priority': 1
        },
        'Cotton': {
            'moisture': (20, 50),
            'temperature': (25, 40),
            'ph': (5.5, 8.0),
            'npk_n': (20, 80),
            'priority': 2
        },
        'Maize': {
            'moisture': (30, 60),
            'temperature': (20, 35),
            'ph': (5.5, 7.5),
            'npk_n': (20, 100),
            'priority': 1
        },
        'Groundnut': {
            'moisture': (30, 50),
            'temperature': (20, 35),
            'ph': (5.0, 7.0),
            'npk_n': (20, 80),
            'priority': 2
        },
        'Sugarcane': {
            'moisture': (70, 100),
            'temperature': (25, 40),
            'ph': (6.0, 7.5),
            'npk_n': (50, 200),
            'priority': 1
        },
        'Mustard': {
            'moisture': (20, 40),
            'temperature': (15, 25),
            'ph': (6.0, 7.5),
            'npk_n': (20, 80),
            'priority': 2
        },
        'Onion': {
            'moisture': (30, 50),
            'temperature': (15, 30),
            'ph': (6.0, 7.5),
            'npk_n': (20, 80),
            'priority': 2
        }
    }
    
    best_crop = None
    best_score = -1
    
    # Score each crop based on how well conditions match
    for crop_name, requirements in crops.items():
        score = 100
        
        # Check moisture
        min_m, max_m = requirements['moisture']
        if soil_moisture < min_m or soil_moisture > max_m:
            score -= 30
        elif soil_moisture < min_m + 10 or soil_moisture > max_m - 10:
            score -= 10
        
        # Check temperature
        min_t, max_t = requirements['temperature']
        if temperature < min_t or temperature > max_t:
            score -= 30
        elif temperature < min_t + 3 or temperature > max_t - 3:
            score -= 10
        
        # Check pH
        min_ph, max_ph = requirements['ph']
        if ph_level < min_ph or ph_level > max_ph:
            score -= 30
        elif ph_level < min_ph + 0.5 or ph_level > max_ph - 0.5:
            score -= 10
        
        # Check nitrogen
        min_n, max_n = requirements['npk_n']
        if npk_n < min_n or npk_n > max_n:
            score -= 20
        
        # Priority boost
        score += requirements['priority'] * 5
        
        # Keep track of best match
        if score > best_score:
            best_score = score
            best_crop = crop_name
    
    # If no good match found, default to something sensible
    if best_crop is None:
        if soil_moisture > 60:
            best_crop = 'Rice'
        elif soil_moisture < 30:
            best_crop = 'Cotton'
        else:
            best_crop = 'Maize'
    
    return best_crop

def get_crop_suitability_score(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k):
    """
    Calculate crop suitability score (0-100) based on soil parameters
    """
    score = 100
    
    # Moisture factor
    if soil_moisture < 20 or soil_moisture > 90:
        score -= 30
    elif soil_moisture < 30 or soil_moisture > 80:
        score -= 15
    
    # Temperature factor
    if temperature < 10 or temperature > 40:
        score -= 30
    elif temperature < 15 or temperature > 35:
        score -= 15
    
    # pH factor
    if ph_level < 4.5 or ph_level > 9.0:
        score -= 30
    elif ph_level < 5.5 or ph_level > 8.0:
        score -= 15
    
    # NPK factor
    if npk_n < 10 or npk_n > 200:
        score -= 10
    if npk_p < 5 or npk_p > 100:
        score -= 10
    if npk_k < 10 or npk_k > 150:
        score -= 10
    
    return max(0, score)
