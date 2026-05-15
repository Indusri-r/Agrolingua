import sys
with open('templates/farm_analysis_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content[:10000])

