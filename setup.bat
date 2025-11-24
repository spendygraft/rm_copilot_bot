@echo off
echo ============================================
echo Telos Email Service Bot - Setup
echo ============================================
echo.

echo [1/3] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/3] Verifying installation...
python -c "from google.oauth2 import service_account; from googleapiclient.discovery import build; print('✅ All dependencies installed successfully!')"
if %errorlevel% neq 0 (
    echo ERROR: Dependency verification failed
    pause
    exit /b 1
)
echo.

echo ============================================
echo ✅ Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Ensure your service account credentials are in: config\telos-email-service-credentials.json
echo 2. Run tests: python test_bot_email.py
echo 3. See README.md for usage examples
echo.
pause
