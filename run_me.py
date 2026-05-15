import os
import sys

# Change to the Agrolinga directory
os.chdir("C:/Users/uma/OneDrive/Desktop/Agrolinga")

# Copy the fixed file
import shutil
src = "templates/farm_analysis_fixed.html"
dst = "templates/farm_analysis.html"

if os.path.exists(dst):
    os.remove(dst)
shutil.copy2(src, dst)
print("File copied successfully!")

# Run the Flask app
os.system("python app.py")
