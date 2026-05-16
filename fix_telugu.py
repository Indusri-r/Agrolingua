import re

# Define proper Telugu translations
new_te = '''            te: {
                analyze: 'విశ్\'లేషణ చేయండి',
                analyzing: 'విశ్\'లేషణ జరుగుతుంది...',
                diseaseDetection: 'రోగ గుర్తింపు',
                cropPrediction: 'పంట ఏబే',
                soilHealth: 'నేల ఆరోగ్యం',
                recommendations: 'సిఫార్సులు',
                noDisease: 'రోగం లేదు',
                healthy: 'ఆరోగ్యం',
                uploadPrompt: 'చెట్టు ఫోటో అప్లోడ్ చేయండి',
                uploadSubtext: 'JPG, PNG 10MB వరకు',
                takePhoto: 'ఫోటో తీయండి',
                uploadImage: 'చెట్టు ఫోటో',
                soilConditions: 'నేల పరిస్థితులు',
                weatherConditions: ' వాతావరణం',
                analysisResults: ' విశ్\'లేషణ ఫలితాలు',
                cropAnalysis: ' ',
                weatherInsights: ' ',
                organicAdvice: ' ',
                soilType: ' ',
                phLevel: 'pH ',
                moisture: ' ',
                nutrients: ' ',
                temperature: ' ',
                humidity: ' ',
                rainfall: ' ',
                season: ' ',
                voiceNote: ' ',
                title: ' ',
                subTitle: ' ',
                selectType: ' ',
                selectSeason: ' ',
                heroSubtitle: 'AI - ',
                formTitle: ' ',
                loadingText: ' ',
                analyzingText: ' '
            }'''

# Fix farm_analysis_new.html
with open('c:/Users/uma/OneDrive/Desktop/Agrolinga/templates/farm_analysis_new.html', 'r', encoding='utf-8') as f:
    content = f.read()

te_start = content.find('te: {')
if te_start == -1:
    print("Could not find te: { in farm_analysis_new.html")
else:
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
    
    new_content = content[:te_start] + new_te + content[te_end:]
    
    with open('c:/Users/uma/OneDrive/Desktop/Agrolinga/templates/farm_analysis_new.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed farm_analysis_new.html")

# Also fix farm_analysis.html
with open('c:/Users/uma/OneDrive/Desktop/Agrolinga/templates/farm_analysis.html', 'r', encoding='utf-8') as f:
    content = f.read()

te_start = content.find('te: {')
if te_start == -1:
    print("Could not find te: { in farm_analysis.html")
else:
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
    
    new_content = content[:te_start] + new_te + content[te_end:]
    
    with open('c:/Users/uma/OneDrive/Desktop/Agrolinga/templates/farm_analysis.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed farm_analysis.html")

