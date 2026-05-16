import os
import shutil

# Copy the fixed file
src = "templates/farm_analysis_fixed.html"
dst = "templates/farm_analysis.html"

if os.path.exists(dst):
    os.remove(dst)
shutil.copy2(src, dst)
print("File copied successfully!")

# Start Flask in background and open browser
import subprocess
import time
import webbrowser

# Start the server
proc = subprocess.Popen(
    ["python", "app.py"],
    cwd="C:/Users/uma/OneDrive/Desktop/Agrolinga",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(3)

# Open browser
webbrowser.open("http://127.0.0.1:5000")
print("Server started and browser opened!")
