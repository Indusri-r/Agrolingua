@echo off
cd /d "C:\Users\uma\OneDrive\Desktop\Agrolinga"
copy /Y "templates\farm_analysis_fixed.html" "templates\farm_analysis.html"
python app.py
