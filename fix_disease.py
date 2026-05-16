import re
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(script_dir, 'app.py')

with open(app_path, 'r') as f:
    content = f.read()

old = '''        raw_disease = process_image(filepath, lang)
        # extract the portion after the pest/disease label if present
        if "Pest/Disease Analysis:" in raw_disease:
            # keep the label + text for clarity
            disease_result = raw_disease.split("Pest/Disease Analysis:", 1)[1].strip()
        else:
            disease_result = raw_disease'''

new = '''        # Use pdr2018_model for better plant/disease detection
        pdr_result = process_plantdoc_image(filepath, lang)
        
        if pdr_result.get('status') == 'success':
            disease_result = pdr_result.get('disease', 'No Disease Detected')
            plant_name = pdr_result.get('plant_name', 'Unknown Plant')
            disease_result = f"{plant_name} - {disease_result}"
        else:
            # Fallback
            raw_disease = process_image(filepath, lang)
            if "Pest/Disease Analysis:" in raw_disease:
                disease_result = raw_disease.split("Pest/Disease Analysis:", 1)[1].strip()
            else:
                disease_result = raw_disease'''

content = content.replace(old, new)

with open(app_path, 'w') as f:
    f.write(content)

print('Done - Disease detection updated to use pdr2018_model')

