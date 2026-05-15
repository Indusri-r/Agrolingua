from gtts import gTTS
import speech_recognition as sr
import os

# Complete translation dictionaries for AgroLingua
# English, Hindi (hi), Telugu (te)
translations = {
    'en': {
        'welcome': 'Welcome to Agrolinga',
        'upload_image': 'Upload Image for Analysis',
        'iot_data': 'IoT Sensor Data',
        'advice': 'Farming Advice',
        'voice_input': 'Voice Input',
        'language': 'Language',
        'submit': 'Submit',
        'soil_moisture': 'Soil Moisture',
        'temperature': 'Temperature',
        'ph_level': 'pH Level',
        'organic_tips': 'Organic Farming Tips',
        'pest_detection': 'Pest and Disease Detection',
        'low_moisture': 'Soil moisture is low. Consider mulching to retain moisture or use drip irrigation.',
        'high_moisture': 'Soil moisture is high. Ensure proper drainage to prevent root rot.',
        'low_temp': 'Temperature is low. Protect crops with row covers or choose cold-tolerant varieties.',
        'high_temp': 'Temperature is high. Provide shade and increase watering frequency.',
        'acidic_ph': 'Soil pH is acidic. Add lime to raise pH for better nutrient availability.',
        'alkaline_ph': 'Soil pH is alkaline. Use sulfur to lower pH.',
        'crop_rotation': 'Practice crop rotation to maintain soil health and prevent pest buildup.',
        'companion_planting': 'Use companion planting to naturally repel pests and attract beneficial insects.',
        'compost': 'Apply compost regularly to improve soil structure and fertility.',
        'biodiversity': 'Encourage biodiversity by planting native species around your crops.',
        'rice_advice': 'For rice, ensure flooded conditions and use organic fertilizers like compost.',
        'wheat_advice': 'For wheat, focus on nitrogen-fixing crops in rotation and organic pest control.',
        'general_crop': 'For general crops, monitor for pests regularly and use neem oil as organic pesticide.',
        'region_monsoon': 'In this region, watch for monsoon patterns and prepare for heavy rainfall.',
        'rainy_weather': 'Rainy weather: Prepare for potential waterlogging and fungal diseases.',
        'dry_weather': 'Dry weather: Increase irrigation and consider drought-resistant varieties.',
        'low_yield': 'Low expected yield: Focus on soil improvement and pest management.',
        'good_yield': 'Good yield potential: Optimize harvesting and storage practices.',
        'high_price': 'High market prices: Consider storage for better returns.',
        'low_price': 'Lower prices: Explore local markets or value-added products.',
        'inorganic_low_moisture': 'Soil moisture is low. Use chemical fertilizers and irrigation systems.',
        'inorganic_high_moisture': 'Soil moisture is high. Use drainage chemicals and adjust irrigation.',
        'inorganic_low_temp': 'Temperature is low. Use chemical growth promoters and protected cultivation.',
        'inorganic_high_temp': 'Temperature is high. Use chemical stress relievers and cooling agents.',
        'inorganic_acidic_ph': 'Soil pH is acidic. Use chemical lime or dolomite.',
        'inorganic_alkaline_ph': 'Soil pH is alkaline. Use chemical sulfur or acidifiers.',
        'chemical_fertilizers': 'Use chemical NPK fertilizers for balanced nutrition.',
        'pesticides': 'Apply chemical pesticides for pest and disease control.',
        'irrigation_systems': 'Implement modern irrigation systems for efficient water use.',
        'market_value': 'Current market value for',
        'current_market_price': 'Current Market Price',
        'nearest_markets': 'Nearest Markets',
        'offline_mode': 'You are offline - Data will sync when connected!',
        'weather_conditions': 'Weather Conditions',
        'yield_prediction': 'Yield Prediction',
        'expected_yield': 'Expected Yield',
        'confidence': 'Confidence',
        'sustainable_farming': 'Sustainable Farming Practices',
        'organic_advisory': 'Organic Advisory Module',
        'crop_suitability': 'Crop Suitability',
        'market_trends': 'Market Trends',
        'soil_health': 'Soil Health',
        'predicted_plant': 'Recommended Crop',
        'no_file_part': 'No file part',
        'no_selected_file': 'No selected file',
        'invalid_file_type': 'Invalid file type',
        'provide_sensor_data': 'Please refresh sensor data first! Click "Refresh Sensor Data" button.',
        'select_image': 'Please select an image first!',
        'voice_error': 'Voice input error. Please try again.',
        'processing': 'Processing... Please wait.',

        # new keys for additional services
        'provide_crop_type': 'Please provide a crop type for biofertilizer suggestion.',
        'biofertilizer_for': 'Recommended biofertilizers for',
        'no_crop_provided': 'No crop type provided. Enter a crop to get suggestions.',
        'ask_for_soil_weather': 'Please provide soil and weather data to proceed.',

        'fungal_disease': 'Potential fungal disease detected (yellow spots). Recommend organic fungicide treatment.',
        'pest_damage': 'Possible pest damage detected (brown spots). Consider neem oil application.',
        'powdery_mildew': 'Powdery mildew detected (white patches). Use sulfur-based fungicide treatment.',
        'healthy_crop': 'No significant pest or disease issues detected. Crop appears healthy.',

        # crop name translations
        'rice': 'Rice',
        'wheat': 'Wheat',
        'cotton': 'Cotton',
        'maize': 'Maize',
        'groundnut': 'Groundnut',
        'sugarcane': 'Sugarcane',
        'mustard': 'Mustard',
        'onion': 'Onion',
        'tomato': 'Tomato',
'potato': 'బంగాళాదుంప',

    },
    'hi': {
        'welcome': 'एग्रोलिंगा में आपका स्वागत है',
        'upload_image': 'विश्लेषण के लिए छवि अपलोड करें',
        'iot_data': 'IoT सेंसर डेटा',
        'advice': 'कृषि सलाह',
        'voice_input': 'वॉइस इनपुट',
        'language': 'भाषा',
        'submit': 'सबमिट करें',
        'soil_moisture': 'मिट्टी की नमी',
        'temperature': 'तापमान',
        'ph_level': 'pH स्तर',
        'organic_tips': 'जैविक कृषि टिप्स',
        'pest_detection': 'कीट और बीमारी का पता लगाना',
        'low_moisture': 'मिट्टी की नमी कम है। नमी बनाए रखने के लिए मल्चिंग करें या ड्रिप सिंचाई का उपयोग करें।',
        'high_moisture': 'मिट्टी की नमी अधिक है। जड़ सड़न को रोकने के लिए उचित जल निकासी सुनिश्चित करें।',
        'low_temp': 'तापमान कम है। फसलों को पंक्ति कवर से बचाएं या ठंड सहने वाली किस्में चुनें।',
        'high_temp': 'तापमान अधिक है। छाया प्रदान करें और पानी देने की आवृत्ति बढ़ाएं।',
        'acidic_ph': 'मिट्टी का pH अम्लीय है। बेहतर पोषक उपलब्धता के लिए pH बढ़ाने के लिए चूना जोड़ें।',
        'alkaline_ph': 'मिट्टी का pH क्षारीय है। pH कम करने के लिए सल्फर का उपयोग करें।',
        'crop_rotation': 'मिट्टी के स्वास्थ्य को बनाए रखने और कीट निर्माण को रोकने के लिए फसल चक्रण का अभ्यास करें।',
        'companion_planting': 'कीटों को स्वाभाविक रूप से दूर करने और लाभकारी कीड़ों को आकर्षित करने के लिए साथी रोपण का उपयोग करें।',
        'compost': 'मिट्टी की संरचना और उर्वरता में सुधार के लिए नियमित रूप से खाद डालें।',
        'biodiversity': 'अपनी फसलों के आसपास देशी प्रजातियों को लगाकर जैव विविधता को प्रोत्साहित करें।',
        'rice_advice': 'चावल के लिए, बाढ़ की स्थिति सुनिश्चित करें और खाद जैसे जैविक उर्वरकों का उपयोग करें।',
        'wheat_advice': 'गेहूं के लिए, चक्रण में नाइट्रोजन-फिक्सिंग फसलों पर ध्यान दें और जैविक कीट नियंत्रण।',
        'general_crop': 'सामान्य फसलों के लिए, नियमित रूप से कीटों की निगरानी करें और जैविक कीटनाशक के रूप में नीम तेल का उपयोग करें।',
        'region_monsoon': 'इस क्षेत्र में, मानसून पैटर्न पर नजर रखें और भारी वर्षा के लिए तैयार रहें।',
        'rainy_weather': 'बारिश का मौसम: संभावित जल जमाव और फंगल रोगों के लिए तैयार रहें।',
        'dry_weather': 'सूखा मौसम: सिंचाई बढ़ाएं और सूखा प्रतिरोधी किस्मों पर विचार करें।',
        'low_yield': 'कम अपेक्षित उपज: मिट्टी सुधार और कीट प्रबंधन पर ध्यान दें।',
        'good_yield': 'अच्छी उपज क्षमता: कटाई और भंडारण प्रथाओं को अनुकूलित करें।',
        'high_price': 'उच्च बाजार मूल्य: बेहतर रिटर्न के लिए भंडारण पर विचार करें।',
        'low_price': 'कम मूल्य: स्थानीय बाजारों या मूल्य-वर्धित उत्पादों का पता लगाएं।',
        'inorganic_low_moisture': 'मिट्टी की नमी कम है। रासायनिक उर्वरकों और सिंचाई प्रणालियों का उपयोग करें।',
        'inorganic_high_moisture': 'मिट्टी की नमी अधिक है। जल निकासी रसायनों का उपयोग करें और सिंचाई को समायोजित करें।',
        'inorganic_low_temp': 'तापमान कम है। रासायनिक विकास प्रोत्साहकों और संरक्षित खेती का उपयोग करें।',
        'inorganic_high_temp': 'तापमान अधिक है। रासायनिक तनाव राहतकर्ताओं और शीतलन एजेंटों का उपयोग करें।',
        'inorganic_acidic_ph': 'मिट्टी का pH अम्लीय है। रासायनिक चूना या डॉलोमाइट का उपयोग करें।',
        'inorganic_alkaline_ph': 'मिट्टी का pH क्षारीय है। रासायनिक सल्फर या अम्लीयकरण का उपयोग करें।',
        'chemical_fertilizers': 'संतुलित पोषण के लिए रासायनिक NPK उर्वरकों का उपयोग करें।',
        'pesticides': 'कीट और बीमारी नियंत्रण के लिए रासायनिक कीटनाशकों का प्रयोग करें।',
        'irrigation_systems': 'कुशल जल उपयोग के लिए आधुनिक सिंचाई प्रणालियों को लागू करें।',
        'market_value': 'के लिए वर्तमान बाजार मूल्य',
        'current_market_price': 'वर्तमान बाजार मूल्य',
        'nearest_markets': 'निकटतम बाजार',
        'offline_mode': 'आप ऑफलाइन हैं - कनेक्ट होने पर डेटा सिंक होगा!',
        'weather_conditions': 'मौसम की स्थिति',
        'yield_prediction': 'उपज पूर्वानुमान',
        'expected_yield': 'अपेक्षित उपज',
        'confidence': 'विश्वास',
        'sustainable_farming': 'टिकाऊ कृषि प्रथाएं',
        'organic_advisory': 'जैविक सलाह मॉड्यूल',
        'crop_suitability': 'फसल की उपयुक्तता',
        'market_trends': 'बाजार के रुझान',
        'soil_health': 'मिट्टी की सेहत',
        'predicted_plant': 'अनुशंसित फसल',
        'no_file_part': 'कोई फाइल भाग नहीं',
        'no_selected_file': 'कोई फाइल नहीं चुनी गई',
        'invalid_file_type': 'अमान्य फाइल प्रकार',

        'provide_crop_type': 'कृपया जैव उर्वरक सुझाव के लिए फसल प्रकार प्रदान करें।',
        'biofertilizer_for': 'के लिए अनुशंसित जैव उर्वरक',
        'no_crop_provided': 'कोई फसल प्रकार प्रदान नहीं किया गया। सुझाव प्राप्त करने के लिए एक फसल दर्ज करें।',
        'ask_for_soil_weather': 'कृपया आगे बढ़ने के लिए मिट्टी और मौसम डेटा प्रदान करें।',

        'fungal_disease': 'संभावित कवक रोग का पता चला (पीले धब्बे)। जैविक कवकनाशक उपचार की सिफारिश की जाती है।',
        'pest_damage': 'संभावित कीट क्षति का पता चला (भूरे धब्बे)। नीम तेल आवेदन पर विचार करें।',
        'powdery_mildew': 'पाउडरी मिल्ड्यू का पता चला (सफेद पैच)। सल्फर-आधारित कवकनाशक उपचार का उपयोग करें।',
        'healthy_crop': 'कोई महत्वपूर्ण कीट या रोग संबंधी समस्या नहीं मिली। फसल स्वस्थ लगती है।',

        # crop name translations
        'rice': 'चावल',
        'wheat': 'गेहूं',
        'cotton': 'कपास',
        'maize': 'मक्का',
        'groundnut': 'मूँगफली',
        'sugarcane': 'गन्ना',
        'mustard': 'सरसों',
        'onion': 'प्याज',
        'tomato': 'टमाटर',
        'potato': 'आलू',
    },
    'te': {
        'welcome': 'అగ్రోలింగా కు స్వాగతం',
'upload_image': 'విశ్లేషణ కోసం చిత్రాన్ని అప్‌లోడ్ చేయండి',
'iot_data': 'ఐఓటీ డేటా',
'advice': 'వ్యవసాయ సలహా',
'voice_input': 'వాయిస్ ఇన్‌పుట్',
'language': 'భాష',
'submit': 'సమర్పించండి',
'soil_moisture': 'మట్టి తేమ',
'temperature': 'ఉష్ణోగ్రత',
'ph_level': 'పీహెచ్ స్థాయి',
'organic_tips': 'సేంద్రీయ వ్యవసాయ సూచనలు',
'pest_detection': 'పురుగు గుర్తింపు',

'low_moisture': 'మట్టిలో తేమ తక్కువగా ఉంది. మల్చింగ్ లేదా డ్రిప్ ఇరిగేషన్ ఉపయోగించండి.',
'high_moisture': 'మట్టిలో తేమ ఎక్కువగా ఉంది. డ్రెయినేజ్‌ను మెరుగుపరచండి.',
'low_temp': 'ఉష్ణోగ్రత తక్కువగా ఉంది. పంటలను కవర్లతో రక్షించండి.',
'high_temp': 'ఉష్ణోగ్రత ఎక్కువగా ఉంది. పంటలకు నీడ కల్పించండి.',

'acidic_ph': 'పీహెచ్ స్థాయి ఆమ్ల స్వభావంలో ఉంది. సున్నం ఉపయోగించండి.',
'alkaline_ph': 'పీహెచ్ స్థాయి క్షార స్వభావంలో ఉంది. సల్ఫర్ ఉపయోగించండి.',

'crop_rotation': 'పంటల మార్పిడి విధానాన్ని అనుసరించండి.',
'companion_planting': 'సహాయక పంటల సాగును అమలు చేయండి.',
'compost': 'కంపోస్ట్‌ను నియమితంగా ఉపయోగించండి.',
'biodiversity': 'జీవ వైవిధ్యాన్ని ప్రోత్సహించండి.',

'rice_advice': 'బియ్యం పంట కోసం నీరు నిల్వ ఉండే పరిస్థితులు కల్పించండి.',
'wheat_advice': 'గోధుమ పంట కోసం నత్రజని స్థిరపరిచే పంటలను ఉపయోగించండి.',
'general_crop': 'సాధారణ పంటల కోసం వేప నూనె ఉపయోగించండి.',

'region_monsoon': 'వర్షాకాల పరిస్థితులను గుర్తుంచుకోండి.',
'rainy_weather': 'వర్షాకాలంలో నీరు నిల్వ కాకుండా జాగ్రత్తలు తీసుకోండి.',
'dry_weather': 'ఎండాకాలంలో నీటి పారుదల పెంచండి.',

'low_yield': 'తక్కువ దిగుబడి: నేల నాణ్యతను మెరుగుపరచండి.',
'good_yield': 'మంచి దిగుబడి: కోత విధానాలను మెరుగుపరచండి.',

'high_price': 'ధర ఎక్కువగా ఉంది: నిల్వ చేయడం పరిగణించండి.',
'low_price': 'ధర తక్కువగా ఉంది: స్థానిక మార్కెట్లను పరిశీలించండి.',

'inorganic_low_moisture': 'రసాయన ఎరువులను ఉపయోగించండి.',
'inorganic_high_moisture': 'డ్రెయినేజ్ రసాయనాలను ఉపయోగించండి.',
'inorganic_low_temp': 'వృద్ధి ప్రోత్సాహకాలను ఉపయోగించండి.',
'inorganic_high_temp': 'స్ట్రెస్ తగ్గించే పదార్థాలను ఉపయోగించండి.',

'inorganic_acidic_ph': 'రసాయన సున్నం ఉపయోగించండి.',
'inorganic_alkaline_ph': 'రసాయన సల్ఫర్ ఉపయోగించండి.',

'chemical_fertilizers': 'రసాయన NPK ఎరువులను ఉపయోగించండి.',
'pesticides': 'రసాయన పురుగుమందులను ఉపయోగించండి.',
'irrigation_systems': 'ఆధునిక నీటి పారుదల వ్యవస్థలను అమలు చేయండి.',

'market_value': 'ప్రస్తుత మార్కెట్ విలువ',
'current_market_price': 'ప్రస్తుత మార్కెట్ ధర',
'nearest_markets': 'సమీప మార్కెట్లు',

'offline_mode': 'మీరు ఆఫ్‌లైన్‌లో ఉన్నారు - కనెక్షన్ వచ్చినప్పుడు డేటా సమకాలీకరణ జరుగుతుంది!',

'weather_conditions': 'వాతావరణ పరిస్థితులు',
'yield_prediction': 'దిగుబడి అంచనా',
'expected_yield': 'అంచనా దిగుబడి',
'confidence': 'నమ్మక స్థాయి',

'sustainable_farming': 'స్థిరమైన వ్యవసాయ పద్ధతులు',
'organic_advisory': 'సేంద్రీయ సలహా విభాగం',
'crop_suitability': 'పంట అనుకూలత',
'market_trends': 'మార్కెట్ ధోరణులు',
'soil_soil_health': 'నేల ఆరోగ్యం',

'predicted_plant': 'సిఫార్సు చేసిన పంట',

'no_file_part': 'ఫైల్ భాగం కనబడలేదు',
'no_selected_file': 'ఏ ఫైల్ ఎంపిక చేయలేదు',
'invalid_file_type': 'చెల్లని ఫైల్ రకం',

'provide_crop_type': 'బయోఫర్టిలైజర్ సూచన కోసం పంట రకం ఇవ్వండి.',
'biofertilizer_for': 'కు అనుకూల బయోఫర్టిలైజర్లు',
'no_crop_provided': 'పంట రకం ఇవ్వలేదు. సూచనలు పొందడానికి పంట పేరు నమోదు చేయండి.',
'ask_for_soil_weather': 'నేల మరియు వాతావరణ వివరాలు ఇవ్వండి.',

'fungal_disease': 'శిలీంధ్ర వ్యాధి (పసుపు మచ్చలు) గుర్తించబడింది. సేంద్రీయ ఫంగిసైడ్ ఉపయోగించండి.',
'pest_damage': 'పురుగు నష్టం (గోధుమ మచ్చలు) గుర్తించబడింది. వేప నూనె పిచికారీ చేయండి.',
'powdery_mildew': 'పౌడరీ మిల్డ్యూ (తెల్ల మచ్చలు) గుర్తించబడింది. సల్ఫర్ ఆధారిత ఫంగిసైడ్ ఉపయోగించండి.',
'healthy_crop': 'గణనీయమైన పురుగు లేదా వ్యాధి సమస్యలు లేవు. పంట ఆరోగ్యంగా ఉంది.',

# crop name translations
'rice': 'బియ్యం',
'wheat': 'గోధుమ',
'cotton': 'పత్తి',
'maize': 'మొక్కజొన్న',
'groundnut': 'వేరుశెనగ',
'sugarcane': 'చెరకు',
'mustard': 'ఆవాలు',
'onion': 'ఉల్లిపాయ',
'tomato': 'టమాటా',
'potato': 'బంగాళాదుంప',
    },
}

# --- dynamic advice translation keys -------------------------------------
extra_keys = {
    'practice_intercropping': {
        'en': 'Practice inter-cropping to maximize land use.',
        'hi': 'भूमि उपयोग को अधिकतम करने के लिए इंटर-क्रॉपिंग का अभ्यास करें।',
        'te': 'జాగ్రత్తగా భూమిని ఉపయోగించడానికి ఇంటర్-క్రాపింగ్ ఆచరణ చేయండి.'
    },
    'apply_biofertilizers': {
        'en': 'Apply biofertilizers like Azotobacter and PSB.',
        'hi': 'एज़ोटोबैक्टर और पीएसबी जैसे जैव उर्वरकों का उपयोग करें।',
        'te': 'అజోటోబాక్టర్ మరియు PSB వంటి బయోఫర్టిలైజర్లు ఉపయోగించండి.'
    },
    'use_trichoderma': {
        'en': 'Use Trichoderma for soil-borne disease control.',
        'hi': 'मृदा जनित रोग नियंत्रण के लिए ट्राइकोडर्मा का उपयोग करें।',
        'te': 'మీ బూరుకు వ్యాధుల నివారణకు ట్రైకొడర్మా ఉపయోగించండి.'
    },
    'use_neem_cake': {
        'en': 'Use neem cake as natural pest repellent.',
        'hi': 'प्राकृतिक कीट निरोधक के रूप में नीम केक का उपयोग करें।',
        'te': 'సేంద్రీయ శత్రు నివారకంగా నీమ్ కేక్ ఉపయోగించండి.'
    },
    'mulching_residues': {
        'en': 'Practice mulching with crop residues.',
        'hi': 'फसल अवशेषों के साथ मल्चिंग का अभ्यास करें।',
        'te': 'పంట పేరుకులుతో మల్చింగ్ సాధన చేయండి.'
    },
    'rainwater_harvesting': {
        'en': 'Set up rainwater harvesting systems.',
        'hi': 'वर्षा जल संचयन प्रणाली स्थापित करें।',
        'te': 'వర్షజల సంరక్షణ వ్యవస్థలను ఏర్పాటు చేయండి.'
    },
    'mulching_organic': {
        'en': 'Use mulching with organic materials to retain soil moisture.',
        'hi': 'मिट्टी की नमी को बनाए रखने के लिए जैविक सामग्री के साथ मल्चिंग करें।',
        'te': 'మట్టిలో తేమ నిల్వ చేయడానికి సేంద్రీయ పదార్థాలతో మల్చింగ్ చేయండి.'
    },
    'drip_irrigation': {
        'en': 'Install drip irrigation system for efficient water use.',
        'hi': 'प्रभावी जल उपयोग के लिए ड्रिप सिंचाई प्रणाली स्थापित करें।',
        'te': 'ఎఫిషియంట్ నీటి వినియోగానికి డ్రిప్ సాగు వ్యవస్థను అమర్చండి.'
    },
    'improve_drainage': {
        'en': 'Improve drainage with raised beds or drainage channels.',
        'hi': 'ऊँचे बेड या जल निकासी चैनलों के साथ जल निकासी में सुधार करें।',
        'te': 'ఎత్తైన బెడ్లు లేదా డ్రెయినేజ్ ఛానల్స్ తో డ్రెయినేజ్ మెరుగుపరచండి.'
    },
    'avoid_overwatering': {
        'en': 'Avoid overwatering - let soil dry slightly between irrigations.',
        'hi': 'अधिक पानी देने से बचें - सिंचाई के बीच मिट्टी को थोड़ा सूखने दें।',
        'te': 'అత్యధిక నీరు ఇవ్వడం నివారించండి - సిచింగ్స్ మధ్య వాటిని కొద్దిగా ఆరిపోనివ్వండి.'
    },
    'row_covers': {
        'en': 'Use row covers or polytunnels to protect crops from cold.',
        'hi': 'ठंड से फसलों को बचाने के लिए रो कवर या पॉलीटन्स का उपयोग करें।',
        'te': 'చల్లుతీ నుండి పంటలను రక్షించడానికి రో కవర్స్ లేదా పోలిటన్నెల్స్ ఉపయోగించండి.'
    },
    'plant_cold_tolerant': {
        'en': 'Plant cold-tolerant varieties like spinach, peas, and lettuce.',
        'hi': 'पालक, मटर और लेट्यूस जैसी ठंड सहने वाली किस्में लगाएं।',
        'te': 'పాలక్, బఠాణీ, లెట్యూస్ వంటి చల్లని సహనశీలకతను కలిగిన వేరైటీలను నాటండి.'
    },
    'shade_nets': {
        'en': 'Provide afternoon shade using shade nets.',
        'hi': 'छायानलों का उपयोग करके दोपहर की छाया प्रदान करें।',
        'te': 'షేడ్ నెట్‌లను ఉపయోగించి మధ్యాహ్నం ఆడును అందించండి.'
    },
    'water_morning_evening': {
        'en': 'Water early morning or late evening to reduce evaporation.',
        'hi': 'वाष्पीकरण को कम करने के लिए सुबह जल्दी या शाम देर से पानी दें।',
        'te': 'ఆవిరివేసే పరిమాణం తగ్గించడానికి ఉదయం తొందరగా లేదా సాయంకాలం ఆలస్యంగా నీళ్లు ఇవ్వండి.'
    },
    'add_lime': {
        'en': 'Add agricultural lime or dolomite to raise pH.',
        'hi': 'pH बढ़ाने के लिए कृषि चूना या डोलोमाइट जोड़ें।',
        'te': 'pH పెంచడానికి వ్యవసాయ లైమ్ లేదా డోలోమైట్ జోడించండి.'
    },
    'use_wood_ash': {
        'en': 'Use wood ash in moderation to balance acidity.',
        'hi': 'अम्लता को संतुलित करने के लिए लकड़ी की राख का प्रयोग करें।',
        'te': 'అమ్లత్వాన్ని సమతుల్యంగా ఉంచడానికి మోస్తరు పరిమాణంలో చెక్క యొక్క బూడిదను ఉపయోగించండి.'
    },
}

# merge dynamic keys into base translations
for key, vals in extra_keys.items():
    for lang_code, text in vals.items():
        translations.setdefault(lang_code, {})[key] = text


def get_translation(key, lang='en'):
    """Get translation for a key in specified language"""
    return translations.get(lang, translations['en']).get(key, key)


def text_to_speech(text, lang='en'):
    """Convert text to speech and save as audio file"""
    try:
        os.makedirs('static', exist_ok=True)
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = f"static/audio_{lang}.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def text_to_speech_parallel(text, lang='en'):
    """Convert text to speech in parallel thread"""

    import threading

    def generate_audio():
        try:
            os.makedirs('static', exist_ok=True)
            tts = gTTS(text=text, lang=lang, slow=False)
            filename = f"static/audio_{lang}.mp3"
            tts.save(filename)
        except Exception as e:
            print(f"TTS Error: {e}")

    thread = threading.Thread(target=generate_audio)
    thread.start()
    thread.join(timeout=10)
    if thread.is_alive():
        return None
    return f"static/audio_{lang}.mp3"


def speech_to_text(lang='en'):
    """Convert speech to text"""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)

        lang_map = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'te': 'te-IN',
        }
        speech_lang = lang_map.get(lang, 'en-US')

        text = recognizer.recognize_google(audio, language=speech_lang)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Could not request results"
    except Exception as e:
        return f"Error: {str(e)}"


def get_supported_languages():
    """Return list of supported language codes"""
    return ['en', 'hi', 'te']


def translate_text(text, lang='en'):
    """Translate a single English text string into the given language."""
    if not text:
        return text

    # If the input is a translation key in target language
    lang_map = translations.get(lang, {})
    if text in lang_map:
        return lang_map[text]

    # Exact match against English values: find the corresponding key
    en_map = translations.get('en', {})
    found_key = None
    for k, v in en_map.items():
        if v == text:
            found_key = k
            break

    if found_key:
        return translations.get(lang, en_map).get(found_key, text)

    # Substring replacement using English phrases found in the text
    translated = text
    for k, v in en_map.items():
        if v and v in translated:
            replacement = translations.get(lang, {}).get(k, v)
            translated = translated.replace(v, replacement)

    try:
        return translated.strip()
    except Exception:
        return translated


def translate_list(text_list, lang='en'):
    """Translate a list of strings into the desired language."""
    if not text_list:
        return []
    return [translate_text(str(item), lang).strip() for item in text_list]

