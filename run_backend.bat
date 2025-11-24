@echo off
echo ========================================
echo Cutting Process Feedback - Backend Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

cd backend

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo ERROR: requirements.txt not found
    pause
    exit /b 1
)

REM Install dependencies if needed (check if Flask is installed)
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing backend dependencies...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found
    if exist .env.example (
        copy .env.example .env
        echo Created .env from .env.example
        echo Please edit backend\.env with your configuration
    )
)

REM Create necessary directories
if not exist uploads\a1 mkdir uploads\a1
if not exist uploads\ghm mkdir uploads\ghm
if not exist uploads\kem mkdir uploads\kem
if not exist logs mkdir logs

echo Starting Flask backend server...
echo Backend will be available at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause

