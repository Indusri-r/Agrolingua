@echo off
cd /d "c:\Users\uma\OneDrive\Desktop\Agrolinga\templates"
move /Y farm_analysis_fixed.html farm_analysis.html
cd /d "c:\Users\uma\OneDrive\Desktop\Agrolinga"
python app.py
