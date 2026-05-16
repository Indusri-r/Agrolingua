import re

# Read the file
with open('c:/Users/uma/OneDrive/Desktop/Agrolinga/templates/farm_analysis_new.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new te translations
new_te = '''            te: {
                analyze: 'Analyze',
                analyzing: 'Analyzing...',
                diseaseDetection: 'Disease Detection',
                cropPrediction: 'Crop Prediction',
                soilHealth: 'Soil Health',
                recommendations: 'Recommendations',
                noDisease: 'No Disease',
                healthy: 'Healthy',
                uploadPrompt: 'Upload Plant Image',
                uploadSubtext: 'JPG, PNG 10MB',
                takePhoto: 'Take Photo',
                uploadImage: 'Upload Plant Image',
                soilConditions: 'Soil Conditions',
                weatherConditions: 'Weather Conditions',
                analysisResults: 'Analysis Results',
                cropAnalysis: 'Crop Analysis',
                weatherInsights: 'Weather',
                organicAdvice: 'Organic Advice',
                soilType: 'Soil Type',
                phLevel: 'pH Level',
                moisture: 'Moisture',
                nutrients: 'NPK',
                temperature: 'Temperature',
                humidity: 'Humidity',
                rainfall: 'Rainfall',
                season: 'Season',
                voiceNote: 'Voice Note',
                title: 'Farm Analysis Form',
                subTitle: 'Farm Analysis',
                selectType: 'Select Type',
                selectSeason: 'Select Season',
                heroSubtitle: 'AI Farming Assistant',
                formTitle: 'Farm Analysis Form',
                loadingText: 'Analyzing...',
                analyzingText: 'Analyzing...'
            }'''

# Find and replace the te: section
# First find where te: { starts
te_start = content.find('te: {')
if te_start == -1:
    print("Could not find te: {")
else:
    # Find the closing };
    # We need to find the }; that closes this object
    # Count braces to find the matching closing brace
    brace_count = 0
    te_end = te_start
    for i in range(te_start, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                te_end = i + 1
                break
    
    # Replace
    new_content = content[:te_start] + new_te + content[te_end:]
    
    # Write back
    with open('c:/Users/uma/OneDrive/Desktop/Agrolinga/templates/farm_analysis_new.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully updated Telugu translations to English")

