import os
import shutil
import subprocess

# Copy the fixed file to farm_analysis.html
src = "templates/farm_analysis_fixed.html"
dst = "templates/farm_analysis.html"

# Remove existing file if exists
if os.path.exists(dst):
    os.remove(dst)

# Copy the fixed file
shutil.copy2(src, dst)
print(f"Copied {src} to {dst}")

# Start the Flask server
print("Starting Flask server...")
subprocess.Popen(["python", "app.py"], 
                 cwd="C:/Users/uma/OneDrive/Desktop/Agrolinga",
                 creationflags=subprocess.CREATE_NEW_CONSOLE)
print("Server started! Open http://127.0.0.1:5000 in your browser")
