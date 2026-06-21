@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo Starting Secure File Vault Web Server...
python app.py
pause
