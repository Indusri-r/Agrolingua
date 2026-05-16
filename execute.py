import os
import subprocess
import sys

# Change to Agrolinga directory
os.chdir("C:/Users/uma/OneDrive/Desktop/Agrolinga")

# First copy the fixed file
import shutil
src = "templates/farm_analysis_fixed.html"
dst = "templates/farm_analysis.html"

if os.path.exists(dst):
    os.remove(dst)
shutil.copy2(src, dst)
print("Fixed file copied!")

# Now run app.py
print("Starting Flask server...")
os.system('start python app.py')
print("Server should be running at http://127.0.0.1:5000")
