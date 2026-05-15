import os
# Read farm_analysis_new.html and save first 5000 chars to a text file
with open('templates/farm_analysis_new.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read(10000)
with open('template_preview.txt', 'w', encoding='utf-8') as out:
    out.write(content)
print("Done")

