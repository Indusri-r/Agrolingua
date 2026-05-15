import random
from languages import get_translation

def get_organic_farming_advice(soil_moisture, temperature, ph_level, lang='te'):
    """
    Generate organic farming advice based on soil conditions.
    Promotes sustainable and eco-friendly farming practices.
    """
    advice = []

    # Soil moisture advice
    if soil_moisture < 30:
        advice.append(get_translation('low_moisture', lang))
        advice.append("🌱 Use mulching with organic materials to retain soil moisture.")
        advice.append("🌱 Install drip irrigation system for efficient water use.")
    elif soil_moisture > 70:
        advice.append(get_translation('high_moisture', lang))
        advice.append("🌱 Improve drainage with raised beds or drainage channels.")
        advice.append("🌱 Avoid overwatering - let soil dry slightly between irrigations.")

    # Temperature advice
    if temperature < 15:
        advice.append(get_translation('low_temp', lang))
        advice.append("🌱 Use row covers or polytunnels to protect crops from cold.")
        advice.append("🌱 Plant cold-tolerant varieties like spinach, peas, and lettuce.")
    elif temperature > 35:
        advice.append(get_translation('high_temp', lang))
        advice.append("🌱 Provide afternoon shade using shade nets.")
        advice.append("🌱 Water early morning or late evening to reduce evaporation.")
        advice.append("🌱 Apply organic mulches to keep soil cool.")

    # pH level advice
    if ph_level < 6.0:
        advice.append(get_translation('acidic_ph', lang))
        advice.append("🌱 Add agricultural lime or dolomite to raise pH.")
        advice.append("🌱 Use wood ash in moderation to balance acidity.")
    elif ph_level > 7.5:
        advice.append(get_translation('alkaline_ph', lang))
        advice.append("🌱 Add organic matter like compost to lower pH naturally.")
        advice.append("🌱 Use gypsum or sulfur to reduce alkalinity.")

    # General organic practices
    general_advice = [
        get_translation('crop_rotation', lang),
        get_translation('companion_planting', lang),
        get_translation('compost', lang),
        get_translation('biodiversity', lang),
    ]
    
    # Add some random organic tips
    # use translation keys for each tip so language selection affects them
    organic_tips = [
        f"🌱 {get_translation('mulching_organic', lang)}",
        f"🌱 {get_translation('drip_irrigation', lang)}",
        f"🌱 {get_translation('improve_drainage', lang)}",
        f"🌱 {get_translation('avoid_overwatering', lang)}",
        f"🌱 {get_translation('row_covers', lang)}",
        f"🌱 {get_translation('plant_cold_tolerant', lang)}",
        f"🌱 {get_translation('shade_nets', lang)}",
        f"🌱 {get_translation('water_morning_evening', lang)}",
        f"🌱 {get_translation('add_lime', lang)}",
        f"🌱 {get_translation('use_wood_ash', lang)}",
        f"🌱 {get_translation('use_neem_cake', lang)}",
        f"🌱 {get_translation('practice_intercropping', lang)}",
        f"🌱 {get_translation('apply_biofertilizers', lang)}",
        f"🌱 {get_translation('use_trichoderma', lang)}",
        f"🌱 {get_translation('mulching_residues', lang)}",
        f"🌱 {get_translation('rainwater_harvesting', lang)}",
    ]
    
    advice.extend(random.sample(general_advice, min(2, len(general_advice))))
    advice.extend(random.sample(organic_tips, min(3, len(organic_tips))))

    return advice

def get_personalized_advice(crop_type, region, lang='te'):
    """
    Generate personalized advice based on crop type and region
    """
    advice = []

    # Crop-specific advice
    if crop_type.lower() == "rice" or "rice" in crop_type.lower():
        advice.append(get_translation('rice_advice', lang))
        advice.append("🌾 Maintain 5-10cm water depth in paddy fields.")
        advice.append("🌾 Use System of Rice Intensification (SRI) method.")
        advice.append("🌾 Apply neem-coated urea for slow nitrogen release.")
    elif crop_type.lower() == "wheat" or "wheat" in crop_type.lower():
        advice.append(get_translation('wheat_advice', lang))
        advice.append("🌾 Sow wheat at optimal spacing for better yield.")
        advice.append("🌾 Apply nitrogen in split doses - 50% at sowing, 50% at crown root initiation.")
    elif crop_type.lower() == "cotton" or "cotton" in crop_type.lower():
        advice.append(get_translation('cotton_advice', lang) if 'cotton_advice' in globals() else "🌱 Cotton requires warm climate (25-35°C).")
        advice.append(get_translation('cotton_water_tip', lang) if 'cotton_water_tip' in globals() else "🌱 Avoid water stagnation - cotton is drought tolerant.")
        advice.append(get_translation('cotton_seeds_tip', lang) if 'cotton_seeds_tip' in globals() else "🌱 Use BT cotton seeds for pest resistance.")
    elif crop_type.lower() == "maize" or "maize" in crop_type.lower():
        advice.append("Maize is a kharif crop requiring warm weather.")
        advice.append("Maintain row spacing of 60-75cm for better growth.")
        advice.append("Maize requires high nitrogen - apply in split doses.")
    else:
        advice.append(get_translation('general_crop', lang))
        advice.append("🌱 Monitor crops regularly for pest and disease attack.")
        advice.append("🌱 Use integrated pest management (IPM) techniques.")

    # Region-specific advice
    if region.lower() in ["telangana", "andhra pradesh", "ap"]:
        advice.append(get_translation('region_monsoon', lang))
        advice.append("📍 Prepare for monsoon by clearing drainage channels.")
        advice.append("📍 Use ridge and furrow method for better water management.")
    elif region.lower() in ["punjab", "haryana"]:
        advice.append("📍 Practice laser land leveling for uniform irrigation.")
        advice.append("📍 Use stubble management techniques.")
    elif region.lower() in ["maharashtra", "gujarat"]:
        advice.append("Use drip irrigation to combat water scarcity.")
        advice.append("Practice dryland farming techniques.")

    return advice

def get_inorganic_farming_advice(soil_moisture, temperature, ph_level, lang='te'):
    """
    Generate conventional/inorganic farming advice
    """
    advice = []

    if soil_moisture < 30:
        advice.append(get_translation('inorganic_low_moisture', lang))
    elif soil_moisture > 70:
        advice.append(get_translation('inorganic_high_moisture', lang))

    if temperature < 15:
        advice.append(get_translation('inorganic_low_temp', lang))
    elif temperature > 35:
        advice.append(get_translation('inorganic_high_temp', lang))

    if ph_level < 6.0:
        advice.append(get_translation('inorganic_acidic_ph', lang))
    elif ph_level > 7.5:
        advice.append(get_translation('inorganic_alkaline_ph', lang))

    # General inorganic advice
    general_advice = [
        get_translation('chemical_fertilizers', lang),
        get_translation('pesticides', lang),
        get_translation('irrigation_systems', lang),
    ]
    
    advice.extend(random.sample(general_advice, min(2, len(general_advice))))

    return advice


def get_biofertilizer_suggestion(crop_type, lang='te'):
    """
    Suggest biofertilizers based on the crop type. Returns a list of biofertilizer names
    and optionally some explanatory text. Language parameter is kept for future
    localization (currently it only affects translated prefixes in the caller).
    """

    # simple mapping of crops to common biofertilizers
    mapping = {
        'rice': ['Azotobacter', 'PSB (Phosphate Solubilizing Bacteria)'],
        'wheat': ['Azospirillum', 'Rhizobium'],
        'maize': ['Azospirillum', 'Phosphobacteria'],
        'cotton': ['Azotobacter', 'Rhizobium'],
        'groundnut': ['Rhizobium', 'PSB'],
        'sugarcane': ['Azospirillum', 'Nitroxin'],
        'mustard': ['Rhizobium', 'PSB'],
        'onion': ['Azotobacter', 'PSB'],
        'tomato': ['Trichoderma', 'Azospirillum'],
        'potato': ['Azospirillum', 'PSB']
    }

    crop_key = crop_type.lower()
    # look for exact or substring match
    for key in mapping.keys():
        if key in crop_key:
            return mapping[key]

    # default suggestion when crop not recognized
    return ['Azotobacter', 'PSB', 'Rhizobium']

def get_weather_yield_price_advice(weather_condition, expected_yield, current_price, lang='te'):
    """
    Generate advice based on weather, yield expectations, and market prices
    """
    advice = []

    # Weather advice
    if weather_condition.lower() == "rainy" or weather_condition.lower() == "monsoon":
        advice.append(get_translation('rainy_weather', lang))
        advice.append("🌧️ Ensure proper drainage to prevent waterlogging.")
        advice.append("🌧️ Apply fungicides preventively for fungal diseases.")
    elif weather_condition.lower() == "dry" or weather_condition.lower() == "drought":
        advice.append(get_translation('dry_weather', lang))
        advice.append("☀️ Use drought-resistant varieties.")
        advice.append("☀️ Apply anti-transpirants to reduce water loss.")
    elif weather_condition.lower() == "cold":
        advice.append("❄️ Protect crops from frost damage.")
        advice.append("❄️ Use anti-frost measures like smoking.")
    elif weather_condition.lower() == "hot":
        advice.append("🔥 Provide irrigation during cooler parts of day.")
        advice.append("🔥 Use anti-transpirants.")

    # Yield advice
    if expected_yield < 50:
        advice.append(get_translation('low_yield', lang))
        advice.append("📈 Focus on soil health improvement.")
        advice.append("📈 Use balanced fertilization.")
    else:
        advice.append(get_translation('good_yield', lang))
        advice.append("📈 Optimize harvesting time for maximum yield.")
        advice.append("📈 Use proper storage techniques.")

    # Price advice
    if current_price > 100:
        advice.append(get_translation('high_price', lang))
        advice.append("💰 Consider staggered selling for better returns.")
    else:
        advice.append(get_translation('low_price', lang))
        advice.append("Explore value-added products.")

    return advice

def get_market_value(crop_type, lang='te'):
    """
    Get current market value for crops
    """
    market_values = {
        'rice': '₹2,000-2,500 per quintal',
        'wheat': '₹1,800-2,200 per quintal',
        'maize': '₹1,500-1,900 per quintal',
        'cotton': '₹5,000-6,000 per quintal',
        'groundnut': '₹4,000-5,500 per quintal',
        'sugarcane': '₹350-400 per quintal',
        'mustard': '₹4,500-5,500 per quintal',
        'onion': '₹1,500-3,000 per quintal',
        'tomato': '₹2,000-4,000 per quintal',
        'potato': '₹1,000-1,500 per quintal',
        'general crop': '₹1,500-2,500 per quintal'
    }

    value = market_values.get(crop_type.lower(), market_values['general crop'])
    return f"{get_translation('market_value', lang)} {crop_type}: {value}"

def get_nearest_markets_and_prices(crop_type, location='telangana', lang='te', city=None):
    """
    Get market information with nearest markets and prices
    Supports city-specific market data for Telangana and Andhra Pradesh
    """
    # City-specific market data for Telangana
    telangana_cities = {
        'hyderabad': [
            {'name': 'Gaddiannaram Market', 'distance': '15 km', 'price': '₹2,100/quintal'},
            {'name': 'Kukatpally Market', 'distance': '18 km', 'price': '₹2,050/quintal'},
            {'name': 'Balanagar Market', 'distance': '20 km', 'price': '₹2,080/quintal'},
            {'name': 'Bowenpally Market', 'distance': '12 km', 'price': '₹2,120/quintal'}
        ],
        'warangal': [
            {'name': 'Warangal Market', 'distance': '5 km', 'price': '₹1,980/quintal'},
            {'name': 'Kazipet Market', 'distance': '12 km', 'price': '₹1,950/quintal'},
            {'name': 'Hanamkonda Market', 'distance': '8 km', 'price': '₹1,970/quintal'},
            {'name': 'Jangaon Market', 'distance': '35 km', 'price': '₹1,920/quintal'}
        ],
        'nizamabad': [
            {'name': 'Nizamabad Market', 'distance': '5 km', 'price': '₹2,000/quintal'},
            {'name': 'Bodhan Market', 'distance': '20 km', 'price': '₹1,980/quintal'},
            {'name': 'Armur Market', 'distance': '25 km', 'price': '₹1,960/quintal'},
            {'name': 'Kamareddy Market', 'distance': '40 km', 'price': '₹1,940/quintal'}
        ],
        'karimnagar': [
            {'name': 'Karimnagar Market', 'distance': '5 km', 'price': '₹1,950/quintal'},
            {'name': 'Sirsilk Market', 'distance': '10 km', 'price': '₹1,930/quintal'},
            {'name': 'Jagtial Market', 'distance': '30 km', 'price': '₹1,910/quintal'},
            {'name': 'Sircilla Market', 'distance': '45 km', 'price': '₹1,890/quintal'}
        ],
        'khammam': [
            {'name': 'Khammam Market', 'distance': '5 km', 'price': '₹1,920/quintal'},
            {'name': 'Kothagudem Market', 'distance': '25 km', 'price': '₹1,900/quintal'},
            {'name': 'Yellandu Market', 'distance': '35 km', 'price': '₹1,880/quintal'},
            {'name': 'Bhadrachalam Market', 'distance': '60 km', 'price': '₹1,850/quintal'}
        ],
        'secunderabad': [
            {'name': 'Secunderabad Market', 'distance': '5 km', 'price': '₹2,150/quintal'},
            {'name': 'Malkajgiri Market', 'distance': '8 km', 'price': '₹2,100/quintal'},
            {'name': 'Trimulgherry Market', 'distance': '10 km', 'price': '₹2,080/quintal'},
            {'name': 'Nacharam Market', 'distance': '12 km', 'price': '₹2,060/quintal'}
        ],
        'mahbubnagar': [
            {'name': 'Mahbubnagar Market', 'distance': '5 km', 'price': '₹1,880/quintal'},
            {'name': 'Gadwal Market', 'distance': '40 km', 'price': '₹1,860/quintal'},
            {'name': 'Wanaparthy Market', 'distance': '35 km', 'price': '₹1,870/quintal'},
            {'name': 'Kollapur Market', 'distance': '50 km', 'price': '₹1,840/quintal'}
        ],
        'karwan': [
            {'name': 'Karwan Market', 'distance': '8 km', 'price': '₹2,050/quintal'},
            {'name': 'Tukaram Gate Market', 'distance': '10 km', 'price': '₹2,030/quintal'},
            {'name': 'Bhavani Market', 'distance': '15 km', 'price': '₹2,010/quintal'},
            {'name': 'Gulzar House Market', 'distance': '12 km', 'price': '₹2,040/quintal'}
        ]
    }

    # City-specific market data for Andhra Pradesh
    andhra_cities = {
        'visakhapatnam': [
            {'name': 'Visakhapatnam Market', 'distance': '5 km', 'price': '₹2,050/quintal'},
            {'name': 'Gajuwaka Market', 'distance': '12 km', 'price': '₹2,030/quintal'},
            {'name': 'Duvvada Market', 'distance': '15 km', 'price': '₹2,000/quintal'},
            {'name': 'Anakapalle Market', 'distance': '30 km', 'price': '₹1,980/quintal'}
        ],
        'vijayawada': [
            {'name': 'Vijayawada Market', 'distance': '5 km', 'price': '₹2,150/quintal'},
            {'name': 'Benz Circle Market', 'distance': '8 km', 'price': '₹2,130/quintal'},
            {'name': 'Guntur Road Market', 'distance': '10 km', 'price': '₹2,100/quintal'},
            {'name': 'Krishna Canal Market', 'distance': '15 km', 'price': '₹2,080/quintal'}
        ],
        'guntur': [
            {'name': 'Guntur Market', 'distance': '5 km', 'price': '₹2,100/quintal'},
            {'name': 'Lakshmipuram Market', 'distance': '8 km', 'price': '₹2,080/quintal'},
            {'name': 'Arundelpet Market', 'distance': '10 km', 'price': '₹2,060/quintal'},
            {'name': 'Brodipet Market', 'distance': '12 km', 'price': '₹2,040/quintal'}
        ],
        'tirupati': [
            {'name': 'Tirupati Market', 'distance': '5 km', 'price': '₹1,950/quintal'},
            {'name': 'Tiruchanur Market', 'distance': '10 km', 'price': '₹1,930/quintal'},
            {'name': 'Renigunta Market', 'distance': '15 km', 'price': '₹1,910/quintal'},
            {'name': 'Srikalahasti Market', 'distance': '35 km', 'price': '₹1,890/quintal'}
        ],
        'nellore': [
            {'name': 'Nellore Market', 'distance': '5 km', 'price': '₹1,920/quintal'},
            {'name': 'Kavali Market', 'distance': '35 km', 'price': '₹1,900/quintal'},
            {'name': 'Ongole Market', 'distance': '65 km', 'price': '₹1,880/quintal'},
            {'name': 'Gudur Market', 'distance': '25 km', 'price': '₹1,910/quintal'}
        ],
        'kadapa': [
            {'name': 'Kadapa Market', 'distance': '5 km', 'price': '₹1,850/quintal'},
            {'name': 'Proddatur Market', 'distance': '40 km', 'price': '₹1,830/quintal'},
            {'name': 'Jammalamadugu Market', 'distance': '60 km', 'price': '₹1,810/quintal'},
            {'name': 'Rayachoty Market', 'distance': '45 km', 'price': '₹1,820/quintal'}
        ],
        'rajahmundry': [
            {'name': 'Rajahmundry Market', 'distance': '5 km', 'price': '₹1,980/quintal'},
            {'name': 'Kakinada Market', 'distance': '60 km', 'price': '₹1,960/quintal'},
            {'name': 'Eluru Market', 'distance': '45 km', 'price': '₹1,940/quintal'},
            {'name': 'Tuni Market', 'distance': '50 km', 'price': '₹1,920/quintal'}
        ],
        'kakinada': [
            {'name': 'Kakinada Market', 'distance': '5 km', 'price': '₹1,960/quintal'},
            {'name': 'Rajahmundry Market', 'distance': '60 km', 'price': '₹1,980/quintal'},
            {'name': 'Pedapuram Market', 'distance': '15 km', 'price': '₹1,940/quintal'},
            {'name': 'Samarlakota Market', 'distance': '20 km', 'price': '₹1,930/quintal'}
        ],
        'anantapur': [
            {'name': 'Anantapur Market', 'distance': '5 km', 'price': '₹1,800/quintal'},
            {'name': 'Dharmavaram Market', 'distance': '40 km', 'price': '₹1,780/quintal'},
            {'name': 'Hindupur Market', 'distance': '55 km', 'price': '₹1,760/quintal'},
            {'name': 'Tadipatri Market', 'distance': '45 km', 'price': '₹1,770/quintal'}
        ],
        'kurnool': [
            {'name': 'Kurnool Market', 'distance': '5 km', 'price': '₹1,820/quintal'},
            {'name': 'Adoni Market', 'distance': '75 km', 'price': '₹1,800/quintal'},
            {'name': 'Nandyal Market', 'distance': '55 km', 'price': '₹1,810/quintal'},
            {'name': 'Yemmiganur Market', 'distance': '65 km', 'price': '₹1,790/quintal'}
        ]
    }

    # State-level market data (fallback when no city specified)
    markets = {
        'telangana': [
            {'name': 'Gaddiannaram Market', 'distance': '10 km', 'price': '₹2,100/quintal'},
            {'name': 'Kukatpally Market', 'distance': '15 km', 'price': '₹2,050/quintal'},
            {'name': 'Warangal Market', 'distance': '150 km', 'price': '₹1,980/quintal'},
            {'name': 'Nizamabad Market', 'distance': '170 km', 'price': '₹2,000/quintal'}
        ],
        'andhra pradesh': [
            {'name': 'Vijayawada Market', 'distance': '250 km', 'price': '₹2,150/quintal'},
            {'name': 'Guntur Market', 'distance': '200 km', 'price': '₹2,100/quintal'},
            {'name': 'Visakhapatnam Market', 'distance': '350 km', 'price': '₹2,050/quintal'},
            {'name': 'Tirupati Market', 'distance': '300 km', 'price': '₹1,950/quintal'}
        ],
        'maharashtra': [
            {'name': 'Vashi Market', 'distance': '400 km', 'price': '₹2,200/quintal'},
            {'name': 'Pune Market', 'distance': '450 km', 'price': '₹2,150/quintal'}
        ],
        'punjab': [
            {'name': 'Azadpur Market', 'distance': '500 km', 'price': '₹2,300/quintal'},
            {'name': 'Ludhiana Market', 'distance': '550 km', 'price': '₹2,250/quintal'}
        ],
        'general': [
            {'name': 'Local Market', 'distance': '5 km', 'price': '₹2,000/quintal'}
        ]
    }

    # Determine which markets to use based on city or state
    if city and city.lower() in telangana_cities:
        location_markets = telangana_cities[city.lower()]
    elif city and city.lower() in andhra_cities:
        location_markets = andhra_cities[city.lower()]
    else:
        # Fall back to state-level or general markets
        location_markets = markets.get(location.lower(), markets['general'])
    
    # Crop-specific prices
    crop_prices = {
        'rice': '₹2,000-2,500/quintal',
        'wheat': '₹1,800-2,200/quintal',
        'maize': '₹1,500-1,900/quintal',
        'cotton': '₹5,000-6,000/quintal',
        'groundnut': '₹4,000-5,500/quintal',
        'sugarcane': '₹350-400/quintal',
        'mustard': '₹4,500-5,500/quintal',
        'general crop': '₹1,500-2,500/quintal'
    }

    current_price = crop_prices.get(crop_type.lower(), crop_prices['general crop'])

    result = f"📊 {get_translation('current_market_price', lang)} {crop_type}: {current_price}\n\n"
    result += f"🏪 {get_translation('nearest_markets', lang)}:\n"
    
    for market in location_markets[:4]:
        result += f"   • {market['name']} ({market['distance']}): {market['price']}\n"

    result += "\n💡 Tip: Compare prices from multiple markets before selling!"

    return result.strip()
