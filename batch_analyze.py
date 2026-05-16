import csv
import os
import json
from app import predict_plant, get_translation, text_to_speech_parallel
from advice import (
    get_organic_farming_advice,
    get_personalized_advice,
    get_nearest_markets_and_prices,
)

# This script reads a CSV dataset with sensor values and runs the
# same logic as the /analyze endpoint without requiring a running
# Flask server or network connectivity. Useful for offline batch
# processing of data.

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'offline_dataset.csv')
# Put output in the static directory (workspace root) so it can be inspected easily
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(STATIC_DIR, 'offline_results.json')

results = []

with open(INPUT_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            lang = row.get('lang', 'en')
            soil_moisture = float(row['soil_moisture'])
            temperature = float(row['temperature'])
            ph_level = float(row['ph_level'])
            npk_n = float(row['npk_n'])
            npk_p = float(row['npk_p'])
            npk_k = float(row['npk_k'])
            ec = float(row['ec'])
            co2 = float(row['co2'])
            region = row.get('region', 'general')
            weather = row.get('weather', 'normal')
        except Exception as e:
            print(f"Skipping row due to parse error: {e}")
            continue

        predicted_crop = predict_plant(soil_moisture, temperature, ph_level, npk_n, npk_p, npk_k, ec, co2)
        crop_translation = get_translation(predicted_crop.lower(), lang)
        if crop_translation == predicted_crop.lower():
            crop_translation = predicted_crop

        organic_advice = get_organic_farming_advice(soil_moisture, temperature, ph_level, lang)
        personalized_advice = get_personalized_advice(predicted_crop, region, lang)
        market_info = get_nearest_markets_and_prices(predicted_crop, region, lang)

        # combine advice text (no TTS generation here for offline simplicity)
        all_advice = organic_advice + personalized_advice + [market_info]
        advice_text = ' '.join(all_advice)

        results.append({
            'input': row,
            'predicted_crop': crop_translation,
            'organic_advice': organic_advice,
            'personalized_advice': personalized_advice,
            'market_info': market_info,
            'combined_text': advice_text,
        })

# write results to JSON
with open(OUTPUT_FILE, 'w', encoding='utf-8') as outf:
    json.dump(results, outf, ensure_ascii=False, indent=2)

print(f"Processed {len(results)} rows. Results written to {OUTPUT_FILE}")
