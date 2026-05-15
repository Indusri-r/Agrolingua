# Agrolinga System Specification

## Overview
Agrolinga is a comprehensive AI-powered agricultural assistant that provides farmers with intelligent farming recommendations through multiple input modalities and output formats. The system integrates deep learning models, sensor data, multilingual support, and market intelligence to deliver personalized farming advice.

## Core Features

### 1. Organic Farming Advice
**Description**: Provides sustainable, eco-friendly farming recommendations based on environmental conditions.

**Inputs**:
- Soil moisture levels (%)
- Temperature (°C)
- Soil pH levels
- Current season
- Crop type

**Outputs**:
- Mulching recommendations
- Irrigation strategies
- pH balancing methods
- Crop rotation suggestions
- Companion planting advice
- Organic pest control methods

**Implementation**: `advice.get_organic_farming_advice()`

### 2. Crop Disease Prediction
**Description**: Uses deep learning models trained on agricultural datasets to identify plant diseases from images.

**Supported Models**:
- Generic multi-crop disease dataset (Wheat, Rice/Paddy, Maize/Corn, Potato)
- Custom trained CNN models (ResNet50 / MobileNetV2 backbones)
- Fallback heuristic-based detection

**Supported Crops**:
- Wheat, Rice/Paddy, Maize/Corn, Potato, plus other crops as the dataset expands

**Disease Detection**:
- Rust, Scab, Bacterial Spot, Gray Leaf Spot, Leaf Blight, Black Rot, Early Blight, Late Blight
- Confidence scores for predictions

**Implementation**: `pdr2018_model.detect_plant_disease()`, `model_stub.predict_disease_nn()`

### 3. Multilingual Support
**Description**: Full localization support for farmer communication in local languages.

**Supported Languages**:
- English (en)
- Hindi (hi)
- Telugu (te)

**Features**:
- UI translation
- Voice input/output in native languages
- Advice translation
- Market information localization

**Implementation**: `languages.py` with translation dictionaries and TTS/STT

### 4. Voice + Text Support
**Description**: Multimodal input/output system for accessibility and ease of use.

**Voice Input**:
- Speech-to-text conversion
- Voice commands for parameter input
- Multilingual voice recognition

**Voice Output**:
- Text-to-speech for advice delivery
- Audio feedback for results
- Offline TTS capability

**Text Input**:
- Manual parameter entry
- Chat-based interaction
- Form-based data collection

**Implementation**: `languages.text_to_speech()`, `languages.speech_to_text()`

### 5. Soil Condition-Based Crop Advice
**Description**: Intelligent crop recommendations based on comprehensive soil analysis.

**Soil Parameters**:
- Soil type (sandy, clay, loam, etc.)
- pH level
- Moisture content
- Nutrient levels (NPK)
- Electrical conductivity (EC)
- Organic matter content

**Recommendation Engine**:
- Suitable crop selection
- Fertilizer requirements
- Irrigation scheduling
- Soil amendment suggestions
- Yield optimization strategies

**Implementation**: `advice.get_personalized_advice()`, `advice.get_weather_yield_price_advice()`

### 6. Market Value Intelligence
**Description**: Real-time market price information and nearby market analysis for optimal selling decisions.

**Features**:
- Current crop prices by region
- Nearby market locations and distances
- Price trends and forecasting
- City-specific market data
- Value-added product suggestions

**Supported Regions**:
- Telangana (Hyderabad, Warangal, Nizamabad, Karimnagar, Khammam)
- Andhra Pradesh
- Karnataka
- Maharashtra

**Price Data**:
- Quintal-based pricing
- Daily market updates
- Regional price variations

**Implementation**: `advice.get_market_value()`, `advice.get_nearest_markets_and_prices()`

## System Architecture

### Backend Components
- **Flask Web Server**: Main application server
- **IoT Integration**: Sensor data collection and storage
- **ML Models**: Disease prediction and crop recommendation engines
- **Database**: SQLite for sensor data and user sessions
- **Translation Engine**: Multilingual text processing
- **TTS/STT Engine**: Voice processing with gTTS and SpeechRecognition

### Frontend Components
- **React Application**: Modern web interface
- **Component Library**: shadcn/ui for consistent UI
- **State Management**: React hooks and context
- **API Integration**: RESTful communication with backend
- **Responsive Design**: Mobile-first approach for field use

### Data Flow
1. **Input Collection**: Image upload, voice input, sensor data, manual entry
2. **Processing Pipeline**:
   - Image analysis for disease detection
   - Soil/weather data processing
   - Multilingual translation
   - Market data retrieval
3. **Recommendation Engine**: AI-powered advice generation
4. **Output Delivery**: Text, voice, and visual results

## API Endpoints

### Core Analysis
```
POST /analyze
- Image analysis with soil/weather context
- Returns: disease detection, crop advice, market info
```

### IoT Data
```
POST /iot-data
- Sensor data submission
GET /iot-data
- Latest sensor readings
GET /iot-history
- Historical sensor data
```

### Voice Processing
```
POST /speech-to-text
- Convert voice to text
POST /text-to-speech
- Convert text to audio
```

### Market Intelligence
```
GET /market-prices/{crop}/{location}
- Current market prices
GET /nearby-markets/{crop}/{city}
- Local market information
```

## Data Models

### Sensor Data
```json
{
  "soil_moisture": 45.2,
  "temperature": 28.5,
  "ph_level": 6.8,
  "npk_n": 120,
  "npk_p": 80,
  "npk_k": 150,
  "ec": 1.2,
  "co2": 420
}
```

### Analysis Request
```json
{
  "imageBase64": "data:image/jpeg;base64,...",
  "soilConditions": "Soil Type: loam, pH: 6.5, Moisture: 40%",
  "weatherConditions": "Temperature: 30°C, Humidity: 65%",
  "language": "te"
}
```

### Analysis Response
```json
{
  "disease": {
    "name": "Early Blight",
    "confidence": 0.89,
    "treatment": "Apply fungicide. Remove infected leaves."
  },
  "advice": [
    "🌱 Use mulching to retain soil moisture",
    "🌱 Apply organic compost for better fertility"
  ],
  "market": {
    "crop": "potato",
    "price": "₹1,200/quintal",
    "nearbyMarkets": [
      {
        "name": "Local Market",
        "distance": "5 km",
        "price": "₹1,250/quintal"
      }
    ]
  },
  "audioUrl": "/static/audio/advice.mp3"
}
```

## Deployment Requirements

### Hardware
- Raspberry Pi or similar for edge deployment
- Camera for image capture
- IoT sensors (moisture, temperature, pH)
- Microphone/speakers for voice I/O

### Software Dependencies
- Python 3.8+
- TensorFlow 2.x
- Flask
- OpenCV
- gTTS
- SpeechRecognition
- SQLite

### Offline Capabilities
- Local model inference
- Cached translations
- Stored market data
- Offline TTS options

## Future Enhancements

### Advanced Features
- Weather API integration
- Satellite imagery analysis
- Blockchain-based traceability
- Farmer community platform
- Mobile app development

### Model Improvements
- Larger datasets for better accuracy
- Multi-crop disease detection
- Real-time model updates
- Federated learning for privacy

### Scalability
- Cloud deployment options
- Multi-region support
- API rate limiting
- Caching strategies

## Quality Assurance

### Testing
- Unit tests for ML models
- Integration tests for API endpoints
- Multilingual content validation
- Offline functionality verification

### Performance Metrics
- Model accuracy > 85%
- Response time < 5 seconds
- Offline operation capability
- Multilingual coverage completeness

This specification defines the comprehensive feature set and technical architecture for Agrolinga, ensuring all requested capabilities are properly integrated and documented.</content>
<parameter name="filePath">c:\Users\uma\OneDrive\Desktop\Agrolinga\SYSTEM_SPECIFICATION.md