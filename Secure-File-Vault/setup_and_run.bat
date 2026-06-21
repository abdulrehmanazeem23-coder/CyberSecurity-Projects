@echo off
cd /d "%~dp0"
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install cryptography bcrypt pyotp qrcode pillow
) else (
    call venv\Scripts\activate.bat
)

python main.py
pause
