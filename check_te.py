import re
with open('c:/Users/uma/OneDrive/Desktop/Agrolinga/templates/farm_analysis_new.html', 'r', encoding='utf-8') as f:
    content = f.read()
    # Find te: { section
    match = re.search(r'te:\s*\{', content)
    if match:
        start = match.start()
        # Find the closing brace
        end = content.find('};', start)
        if end > 0:
            print(content[start:end+2])

