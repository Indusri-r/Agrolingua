#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(r"C:\Users\uma\OneDrive\Desktop\Agrolinga")

# Copy file
import shutil
shutil.copy(r"templates\farm_analysis_fixed.html", r"templates\farm_analysis.html")

# Start subprocess
subprocess.Popen([sys.executable, "app.py"])
