from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import random
from model_stub import process_image, get_dataset_statistics
from iot import init_db, save_sensor_data, get_latest_sensor_data, get_sensor_history
from advice import (
    get_organic_farming_advice,
    get_personalized_advice,
    get_weather_yield_price_advice,
    get_inorganic_farming_advice,
    get_market_value,
    get_nearest_markets_and_prices,
    get_biofertilizer_suggestion
)
from languages import get_translation, text_to_speech, text_to_speech_parallel, speech_to_text, get_supported_languages
from languages import translate_list
from plant_prediction import predict_plant

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize database
init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    return render_template('farm_analysis_v2.html', lang=lang)

@app.route('/v2')
def index_v2():
    """Farm Analysis V2 - Enhanced version with improved UI"""
    lang = request.args.get('lang', 'en')
    return render_template('farm_analysis_v2.html', lang=lang)

@app.route('/iot-data', methods=['GET', 'POST'])
def iot_data():
    if request.method == 'POST':
        data = request.get_json()
        save_sensor_data(data['soil_moisture'], data['temperature'], data['ph_level'],
                        data.get('npk_n'), data.get('npk_p'), data.get('npk_k'),
                        data.get('ec'), data.get('co2'))
        return jsonify({'status': 'success'})
    else:
        data = get_latest_sensor_data()
        if data:
            return jsonify(data)
        else:
            return jsonify([None, None, 50, 25, 7.0, 40, 20, 30, 1.0, 400])  # Default values if no data

@app.route('/weather')
def weather():
    """
    Get weather data - Mock implementation for demonstration
    In production, integrate with weather API like OpenWeatherMap
    """
    # Mock weather data - in production, fetch from weather API
    weather_conditions = [
        {'temperature': 28, 'humidity': 65, 'rainfall': 5, 'wind_speed': 12, 'forecast': 'Partly Cloudy'},
        {'temperature': 25, 'humidity': 75, 'rainfall': 15, 'wind_speed': 8, 'forecast': 'Rainy'},
        {'temperature': 32, 'humidity': 45, 'rainfall': 0, 'wind_speed': 15, 'forecast': 'Sunny'},
        {'temperature': 30, 'humidity': 55, 'rainfall': 2, 'wind_speed': 10, 'forecast': 'Cloudy'},
        {'temperature': 26, 'humidity': 80, 'rainfall': 25, 'wind_speed': 6, 'forecast': 'Heavy Rain'},
    ]
    current_weather = random.choice(weather_conditions)
    return jsonify(current_weather)

@app.route('/yield-prediction')
def yield_prediction():
    """
    Predict expected yield based on soil and weather conditions
    """
    # require input before predicting
    if not request.args.get('soil_moisture') or not request.args.get('temperature'):
        lang = request.args.get('lang', 'te')
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})
    
    try:
        soil_moisture = float(request.args.get('soil_moisture'))
        temperature = float(request.args.get('temperature'))
    except ValueError:
        lang = request.args.get('lang', 'te')
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})
    
    # Simple yield prediction algorithm based on conditions
    # In production, use ML model for accurate predictions
    base_yield = 50  # quintals per acre
    
    # Adjust based on moisture
    if 40 <= soil_moisture <= 70:
        moisture_factor = 1.0
    elif soil_moisture < 40:
        moisture_factor = 0.7
    else:
        moisture_factor = 0.8
    
    # Adjust based on temperature
    if 20 <= temperature <= 30:
        temp_factor = 1.0
    elif temperature < 20:
        temp_factor = 0.8
    else:
        temp_factor = 0.75
    
    expected_yield = int(base_yield * moisture_factor * temp_factor)
    confidence = int(70 + random.randint(0, 25))
    
    return jsonify({
        'expected_yield': expected_yield,
        'confidence': confidence
    })

@app.route('/organic-advice')
def organic_advice():
    """
    Dedicated endpoint for organic farming advice
    Promotes sustainable and eco-friendly farming practices
    """
    lang = request.args.get('lang', 'te')
    # require sensor data inputs before giving advice
    required = ['soil_moisture', 'temperature', 'ph_level']
    missing = [p for p in required if request.args.get(p) is None]
    if missing:
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})
    
    try:
        soil_moisture = float(request.args.get('soil_moisture'))
        temperature = float(request.args.get('temperature'))
        ph_level = float(request.args.get('ph_level'))
    except ValueError:
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})
    
    # Get organic-specific advice
    organic_advice_list = get_organic_farming_advice(soil_moisture, temperature, ph_level, lang)
    
    # Add sustainable farming practices
    sustainable_practices = [
        get_translation('crop_rotation', lang),
        get_translation('companion_planting', lang),
        get_translation('compost', lang),
        get_translation('biodiversity', lang),
    ]
    
    # Add soil health tips
    if soil_moisture < 40:
        organic_advice_list.append(get_translation('low_moisture', lang))
    elif soil_moisture > 70:
        organic_advice_list.append(get_translation('high_moisture', lang))
    
    # Add temperature-specific organic advice
    if temperature < 15:
        organic_advice_list.append(get_translation('low_temp', lang))
    elif temperature > 35:
        organic_advice_list.append(get_translation('high_temp', lang))
    
    # Add pH-specific advice
    if ph_level < 6.0:
        organic_advice_list.append(get_translation('acidic_ph', lang))
    elif ph_level > 7.5:
        organic_advice_list.append(get_translation('alkaline_ph', lang))
    
    return jsonify({
        'advice': organic_advice_list,
        'type': 'organic'
    })

@app.route('/market-info')
def market_info():
    """
    Get market information for crops
    """
    lang = request.args.get('lang', 'te')
    region = request.args.get('region', 'telangana')
    city = request.args.get('city', None)
    
    # Get market info
    market_text = get_nearest_markets_and_prices('general crop', region, lang, city)
    
    return jsonify({
        'market_info': market_text
    })

@app.route('/predict-plant')
def predict_plant_route():
    lang = request.args.get('lang', 'te')
    # check for required sensor inputs and if not present ask the user
    required = ['soil_moisture', 'temperature', 'ph_level', 'npk_n', 'npk_p', 'npk_k', 'ec', 'co2']
    missing = [p for p in required if request.args.get(p) is None]
    if missing:
        # if any of the critical soil/weather values are missing, send a prompt
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})
    # since we already ensured values are present, convert safely
    try:
        soil_moisture = float(request.args.get('soil_moisture'))
        temperature = float(request.args.get('temperature'))
        ph_level = float(request.args.get('ph_level'))
        npk_n = float(request.args.get('npk_n'))
        npk_p = float(request.args.get('npk_p'))
        npk_k = float(request.args.get('npk_k'))
        ec = float(request.args.get('ec'))
        co2 = float(request.args.get('co2'))
    except ValueError:
        # invalid numeric input
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})

    # Debug: show raw + parsed inputs and which model path is used
    print("[DEBUG] /predict-plant raw args:", {k: request.args.get(k) for k in ['soil_moisture','temperature','ph_level','npk_n','npk_p','npk_k','ec','co2'] if k in request.args})
    print("[DEBUG] /predict-plant parsed:", {
        'soil_moisture': soil_moisture,
        'temperature': temperature,
        'ph_level': ph_level,
        'npk_n': npk_n,
        'npk_p': npk_p,
        'npk_k': npk_k,
        'ec': ec,
        'co2': co2,
        'lang': lang
    })

    predicted_plant = predict_plant(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2)
    print("[DEBUG] /predict-plant predicted_plant:", predicted_plant)

    # translate the predicted plant name if we have a translation entry

    plant_translation = get_translation(predicted_plant.lower(), lang)
    if plant_translation == predicted_plant.lower():
        # translation not found, fall back to original
        plant_translation = predicted_plant
    prediction_text = f"{get_translation('predicted_plant', lang)}: {plant_translation}"
    
    # Add additional crop recommendations
    crop_recommendations = []
    if soil_moisture > 60 and temperature > 20:
        crop_recommendations.append("Rice - Best for high moisture conditions")
    if 40 <= soil_moisture <= 60 and 20 <= temperature <= 30:
        crop_recommendations.append("Wheat - Suitable for moderate conditions")
    if soil_moisture < 40:
        crop_recommendations.append("Cotton - Drought-tolerant crop")
    if ph_level < 6.0:
        crop_recommendations.append("Groundnut - Thrives in acidic soils")
    
    if crop_recommendations:
        prediction_text += "\n" + "\n".join(crop_recommendations)

    # also include audio version of the prediction for voice assistance
    audio_file = text_to_speech_parallel(prediction_text, lang)
    print('[DEBUG] /predict-plant audio_file:', audio_file)
    audio_url = f'/{audio_file}' if audio_file else None

    return jsonify({
        'prediction': prediction_text,
        'audio_url': audio_url
    })


@app.route('/biofertilizer')
def biofertilizer():
    """
    Suggest biofertilizers based on a crop type provided by the user.
    """

    lang = request.args.get('lang', 'te')
    crop = request.args.get('crop')
    if not crop:
        error = get_translation('provide_crop_type', lang)
        return jsonify({'error': error})

    suggestions = get_biofertilizer_suggestion(crop, lang)
    # build a response string that can be spoken
    text = f"{get_translation('biofertilizer_for', lang)} {crop}: {', '.join(suggestions)}"
    audio_file = text_to_speech_parallel(text, lang)
    audio_url = f'/{audio_file}' if audio_file else None
    return jsonify({
        'crop': crop,
        'suggestions': suggestions,
        'text': text,
        'audio_url': audio_url
    })

@app.route('/advice')
def get_advice():
    lang = request.args.get('lang', 'te')
    # require sensor data inputs before giving advice
    required = ['soil_moisture', 'temperature', 'ph_level', 'npk_n', 'npk_p', 'npk_k', 'ec', 'co2']
    missing = [p for p in required if request.args.get(p) is None]
    if missing:
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})
    
    try:
        soil_moisture = float(request.args.get('soil_moisture'))
        temperature = float(request.args.get('temperature'))
        ph_level = float(request.args.get('ph_level'))
        npk_n = float(request.args.get('npk_n'))
        npk_p = float(request.args.get('npk_p'))
        npk_k = float(request.args.get('npk_k'))
        ec = float(request.args.get('ec'))
        co2 = float(request.args.get('co2'))
    except ValueError:
        error = get_translation('ask_for_soil_weather', lang)
        return jsonify({'error': error})
    
    region = request.args.get('region', 'general')
    weather = request.args.get('weather', 'normal')
    expected_yield = float(request.args.get('yield', 70)) if request.args.get('yield') else 70
    current_price = float(request.args.get('price', 80)) if request.args.get('price') else 80
    predicted_plant_param = request.args.get('predicted_plant')

    # Predict the plant type based on sensor data if not provided
    if predicted_plant_param:
        predicted_plant = predicted_plant_param
    else:
        predicted_plant = predict_plant(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2)

    organic_advice = get_organic_farming_advice(soil_moisture, temperature, ph_level, lang)
    inorganic_advice = get_inorganic_farming_advice(soil_moisture, temperature, ph_level, lang)
    personalized_advice = get_personalized_advice(predicted_plant, region, lang)
    weather_advice = get_weather_yield_price_advice(weather, expected_yield, current_price, lang)
    market_info = get_nearest_markets_and_prices(predicted_plant, region, lang)

    # Combine all advice into a single text for TTS
    all_advice = organic_advice + inorganic_advice + personalized_advice + weather_advice + [market_info]
    advice_text = ' '.join(all_advice)
    audio_file = text_to_speech_parallel(advice_text, lang)

    if audio_file is None:
        audio_url = None
    else:
        audio_url = f'/{audio_file}'

    return jsonify({
        'audio_url': audio_url,
        'market_info': market_info,
        'advice_text': advice_text
    })

@app.route('/voice-input', methods=['POST'])
def voice_input():
    lang = request.form.get('lang', 'en')
    text = speech_to_text(lang)
    return jsonify({'text': text, 'lang': lang})

@app.route('/text-to-speech')
def tts():
    text = request.args.get('text', 'Hello')
    lang = request.args.get('lang', 'en')
    audio_file = text_to_speech(text, lang)
    return jsonify({'audio_url': f'/{audio_file}'})

@app.route('/languages')
def languages():
    return jsonify(get_supported_languages())

@app.route('/analyze', methods=['POST'])
def analyze_farm():
    """
    Comprehensive farm analysis endpoint.
    Accepts: image upload, IoT sensor data, weather data, language preference
    Returns: disease prediction + organic advice + market value + audio responses
    """
    try:
        lang = request.form.get('lang', 'te')
        print(f"[DEBUG] Analyze endpoint received language: {lang}")
        print(f"[DEBUG] Form data keys: {list(request.form.keys())}")
        print(f"[DEBUG] Language value from form: '{lang}'")
        
        # 1. VALIDATE AND PROCESS IMAGE
        if 'image' not in request.files:
            return jsonify({'error': get_translation('no_file_part', lang)}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': get_translation('no_selected_file', lang)}), 400
        
        if not allowed_file(image_file.filename):
            return jsonify({'error': get_translation('invalid_file_type', lang)}), 400
        
        # Save and process image
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        # process_image currently returns a multi-line string with image info
        # followed by "\nPest/Disease Analysis: ...". For user-facing output
        # and speech we only want the disease summary, not the image metadata.
        # Use the crop disease image model (generic multi-crop dataset).
        disease_result_dict = process_image(filepath, lang)

        if disease_result_dict.get('status') == 'success':

            plant_name = disease_result_dict.get(
                'plant_name',
                'Unknown Plant'
            )

            disease = disease_result_dict.get(
                'disease',
                'No Disease Detected'
            )

            confidence = disease_result_dict.get(
                'confidence',
                0
            )

            # Fix numeric prediction issue
            if str(disease).isdigit():
                disease = "Unknown Disease"

            # Translate plant name
            translated_plant = get_translation(
                plant_name.lower(),
                lang
            )

            if translated_plant == plant_name.lower():
                translated_plant = plant_name

            # Translate disease name
            translated_disease = get_translation(
                disease.lower(),
                lang
            )

            if translated_disease == disease.lower():
                translated_disease = disease

            # Final output
            disease_result = (
                f"{translated_plant} - "
                f"{translated_disease} "
                f"({confidence:.1f}%)"
            )

        else:

            disease_result = disease_result_dict.get(
                'disease',
                'Analysis failed'
            )
        
      
        
        # 2. VALIDATE AND PROCESS IOT SENSOR DATA
        required_iot = ['soil_moisture', 'temperature', 'ph_level', 'npk_n', 'npk_p', 'npk_k', 'ec', 'co2']
        missing_iot = [p for p in required_iot if not request.form.get(p)]
        if missing_iot:
            return jsonify({'error': get_translation('ask_for_soil_weather', lang)}), 400
        
        try:
            soil_moisture = float(request.form.get('soil_moisture'))
            temperature = float(request.form.get('temperature'))
            ph_level = float(request.form.get('ph_level'))
            npk_n = float(request.form.get('npk_n'))
            npk_p = float(request.form.get('npk_p'))
            npk_k = float(request.form.get('npk_k'))
            ec = float(request.form.get('ec'))
            co2 = float(request.form.get('co2'))
        except ValueError as ve:
            return jsonify({'error': f"Invalid number format: {str(ve)}"}), 400
        
        # 3. PROCESS OPTIONAL WEATHER DATA
        weather = request.form.get('weather', 'normal')
        region = request.form.get('region', 'general')
        
# 4. PREDICT CROP TYPE - Use image-based crop detection if available, fallback to sensor data
        image_plant_name = disease_result_dict.get('plant_name', '') if disease_result_dict.get('status') == 'success' else ''
        
        # If image-based crop detection returns a reliable plant name, use it.
        if image_plant_name and image_plant_name != 'Unknown Plant' and image_plant_name != 'Healthy Plant':
            predicted_crop = image_plant_name
            print(f"[DEBUG] Using image-detected plant: {predicted_crop}")
        else:
            predicted_crop = predict_plant(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2)
            print(f"[DEBUG] Using sensor-based crop prediction: {predicted_crop}")
        
        crop_translation = get_translation(predicted_crop.lower(), lang)
        if crop_translation == predicted_crop.lower():
            crop_translation = predicted_crop
        
        # 5. GET ORGANIC FARMING ADVICE
        try:
            organic_advice = get_organic_farming_advice(soil_moisture, temperature, ph_level, lang)
            # Ensure it's a list of strings
            organic_advice = [str(item) for item in organic_advice] if organic_advice else []
            organic_advice = translate_list(organic_advice, lang)
        except Exception as oe:
            print(f"Error getting organic advice: {oe}")
            organic_advice = ["Could not generate organic advice"]
        
        # 6. GET PERSONALIZED ADVICE for predicted crop
        try:
            personalized_advice = get_personalized_advice(predicted_crop, region, lang)
            # Ensure it's a list of strings
            personalized_advice = [str(item) for item in personalized_advice] if personalized_advice else []
            personalized_advice = translate_list(personalized_advice, lang)
        except Exception as pe:
            print(f"Error getting personalized advice: {pe}")
            personalized_advice = ["Could not generate personalized advice"]
        
        # 7. GET MARKET VALUE AND NEARBY MARKETS
        # Get city from form data for Telangana/AP specific markets
        city = request.form.get('city', None)
        try:
            market_info = get_nearest_markets_and_prices(predicted_crop, region, lang, city)
            market_info = str(market_info) if market_info else "Market information unavailable"
        except Exception as me:
            print(f"Error getting market info: {me}")
            market_info = "Market information unavailable"
        
        # 8. COMBINE ALL ADVICE FOR VOICE OUTPUT
        try:
            advice_items = []
            advice_items.append(f"{get_translation('predicted_plant', lang)}: {crop_translation}")
            advice_items.append(f"{get_translation('pest_detection', lang)}: {disease_result}")
            advice_items.append(f"{get_translation('organic_advisory', lang)}:")
            if organic_advice:
                advice_items.extend([str(item) for item in organic_advice[:3]])
            all_advice_text = "\n".join(advice_items) + f"\n{get_translation('market_trends', lang)}: {market_info}"
        except Exception as ae:
            print(f"Error combining advice: {ae}")
            all_advice_text = f"Disease: {disease_result}\nCrop: {crop_translation}\nMarket: {market_info}"
        
        # 9. GENERATE AUDIO OUTPUT
        # Try asynchronous generation first, then fall back to synchronous
        audio_file = text_to_speech_parallel(all_advice_text, lang)
        if audio_file is None:
            try:
                audio_file = text_to_speech(all_advice_text, lang)
            except Exception as tte:
                print(f"Synchronous TTS failed: {tte}")
                audio_file = None
        audio_url = f'/{audio_file}' if audio_file else None
        
        # 10. SAVE IOT DATA to database
        save_sensor_data(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2)
        
        # 11. RETURN COMPREHENSIVE RESPONSE
        return jsonify({
            'status': 'success',
            'lang': lang,
            'disease_prediction': disease_result,
            'predicted_crop': crop_translation,
            'soil_analysis': {
                'moisture': soil_moisture,
                'temperature': temperature,
                'ph_level': ph_level,
                'npk': {'n': npk_n, 'p': npk_p, 'k': npk_k},
                'ec': ec,
                'co2': co2
            },
            'organic_advice': organic_advice,
            'personalized_advice': personalized_advice,
            'market_info': market_info,
            'combined_advice_text': all_advice_text,
            'audio_url': audio_url,
            'voice_support': True,
            'regional_language': lang in get_supported_languages()
        }), 200
    
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}"
        print(f"Analyze endpoint error: {traceback.format_exc()}")
        return jsonify({'error': error_msg}), 500

def analyze_environmental_conditions(soil_moisture, temperature, humidity, weather):
    """Analyze environmental conditions and their effect on plant diseases."""
    factors = []
    risk_level = "Low"
    
    if soil_moisture > 70:
        factors.append("High soil moisture - High risk of fungal diseases")
        risk_level = "High"
    elif soil_moisture > 60:
        factors.append("Moderate-high soil moisture - Medium risk of fungal diseases")
        if risk_level == "Low":
            risk_level = "Medium"
    
    if soil_moisture < 30:
        factors.append("Low soil moisture - Plants stressed, vulnerable to diseases")
        factors.append("Increase irrigation to improve plant health")
    
    if temperature > 30:
        factors.append("High temperature - Promotes rapid disease spread")
        if risk_level == "Low":
            risk_level = "Medium"
    elif temperature < 15:
        factors.append("Low temperature - Slow plant growth, potential cold damage")
    
    if humidity > 80:
        factors.append("High humidity - Ideal for fungal growth")
        if risk_level != "High":
            risk_level = "Medium"
    elif humidity < 40:
        factors.append("Low humidity - Plants may be stressed")
    
    if weather == 'rainy':
        factors.append("Rainy weather - Disease spread likely, inspect regularly")
        risk_level = "High"
    elif weather == 'dry':
        factors.append("Dry conditions - Monitor irrigation closely")
    
    return {
        'risk_level': risk_level,
        'factors': factors,
        'advice': get_environmental_advice(soil_moisture, temperature, humidity, weather)
    }

def get_environmental_advice(soil_moisture, temperature, humidity, weather):
    """Generate advice based on environmental conditions."""
    advice = []
    
    if soil_moisture < 40:
        advice.append("Increase watering frequency")
        advice.append("Apply mulch to retain soil moisture")
    elif soil_moisture > 70:
        advice.append("Improve drainage to prevent root rot")
        advice.append("Avoid overhead watering")
    
    if temperature > 35:
        advice.append("Provide afternoon shade")
        advice.append("Water during cooler hours")
    elif temperature < 10:
        advice.append("Use row covers to protect plants")
        advice.append("Choose cold-tolerant varieties")
    
    if humidity > 75:
        advice.append("Improve air circulation")
        advice.append("Apply preventive fungicide")
    
    if weather == 'rainy':
        advice.append("Inspect plants for disease signs")
        advice.append("Remove infected leaves promptly")
    
    return advice

def combine_predictions(image_result, env_result):
    """Combine image disease analysis with environmental analysis for final prediction."""
    disease = image_result.get('disease', 'Unknown')
    confidence = image_result.get('confidence', 0)
    risk_level = env_result.get('risk_level', 'Low')
    
    if risk_level == 'High':
        adjusted_confidence = min(95, confidence + 10)
        prediction = f"High risk: {disease}. Environmental conditions favor disease development."
    elif risk_level == 'Medium':
        adjusted_confidence = min(90, confidence + 5)
        prediction = f"Medium risk: {disease}. Monitor closely."
    else:
        adjusted_confidence = confidence
        prediction = f"Low risk: {disease}. Continue regular care."
    
    return {
        'prediction': prediction,
        'adjusted_confidence': adjusted_confidence,
        'risk_level': risk_level
    }

@app.route('/dataset-info')
def dataset_info():
    """Get information about the currently configured crop disease dataset."""
    stats = get_dataset_statistics()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
