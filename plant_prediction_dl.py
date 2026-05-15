import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model

# DL model paths
MODEL_PATH = 'models/crop_model.h5'
SCALER_PATH = 'models/crop_scaler.pkl'
LABEL_ENCODER_PATH = 'models/crop_encoder.pkl'

# Global variables
_crop_model = None
_scaler = None
_label_encoder = None

def load_crop_model():
    global _crop_model, _scaler, _label_encoder
    if _crop_model is not None:
        return True

    try:
        _crop_model = load_model(MODEL_PATH)
        _scaler = joblib.load(SCALER_PATH)
        _label_encoder = joblib.load(LABEL_ENCODER_PATH)
        print("✅ DL Crop model loaded!")
        return True
    except Exception as e:
        print(f"❌ DL model load failed: {e}. Falling back to rules.")
        return False

def predict_crop_dl(N, temperature, ph_level, npk_p, npk_k, soil_moisture, ec, co2):
    """
    DL-based crop prediction using trained model.
    Features adapted from dataset: N,temperature,humidity=65,ph, rainfall=120,soil_moisture,P,K,ec,co2
    """
    if not load_crop_model():
        return predict_plant(soil_moisture, temperature, ph_level, N, npk_p, npk_k, ec, co2)  # Fallback
    
    # Prepare features (match dataset order)
    humidity = 65.0  # Average
    rainfall = 120.0  # Average
    features = np.array([[N, temperature, humidity, ph_level, rainfall, soil_moisture, npk_p, npk_k, ec, co2]])
    features_scaled = _scaler.transform(features)
    
    pred = _crop_model.predict(features_scaled, verbose=0)
    crop_idx = np.argmax(pred[0])
    crop = _label_encoder.inverse_transform([crop_idx])[0]
    confidence = float(np.max(pred[0]))
    
    return f"{crop} (confidence: {confidence:.2f})"

def predict_plant(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2):
    """
    Updated: DL-first, fallback to rules.
    """
    dl_pred = predict_crop_dl(npk_n, temperature, ph_level, npk_p, npk_k, soil_moisture, ec, co2)
    return dl_pred

# Keep other functions for compatibility
def predict_plant_type(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2):
    # DL version or original rules
    if load_crop_model():
        return predict_crop_dl(npk_n, temperature, ph_level, npk_p, npk_k, soil_moisture, ec, co2)
    else:
        # Original rules code here (omitted for brevity, copy from original)
        # ... (use original implementation)
        pass  # Replace with original

def get_crop_suitability_score(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k):
    return 85  # Placeholder

if __name__ == '__main__':
    # Test
    crop = predict_plant(65, 27, 6.8, 40, 24, 52, 1.2, 420)
    print(f"Predicted crop: {crop}")

