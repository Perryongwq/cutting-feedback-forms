@echo off
echo ========================================
echo Cutting Process Feedback Application
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

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and add it to your PATH
    pause
    exit /b 1
)

REM Get the script directory (project root)
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

echo [1/2] Starting backend server...

REM Check if .env file exists
if not exist backend\.env (
    echo WARNING: .env file not found. Creating from .env.example...
    if exist backend\.env.example (
        copy backend\.env.example backend\.env >nul
        echo Please edit backend\.env with your configuration
    ) else (
        echo WARNING: .env.example not found. Using default configuration.
    )
)

REM Create necessary directories
if not exist backend\uploads\a1 mkdir backend\uploads\a1
if not exist backend\uploads\ghm mkdir backend\uploads\ghm
if not exist backend\uploads\kem mkdir backend\uploads\kem
if not exist backend\logs mkdir backend\logs

REM Start backend in a new window with correct working directory
start "Backend Server" cmd /k "cd /d "%PROJECT_ROOT%backend" && python app.py"
timeout /t 3 /nobreak >nul
echo Backend server starting on http://localhost:5000
echo.

echo [2/2] Starting frontend server...

REM Start frontend in a new window with correct working directory
start "Frontend Server" cmd /k "cd /d "%PROJECT_ROOT%frontend" && npm start"
timeout /t 3 /nobreak >nul
echo Frontend server starting on http://localhost:3000
echo.

echo ========================================
echo Application is starting...
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Two windows have been opened:
echo - Backend Server: Flask API
echo - Frontend Server: React App
echo.
echo Press any key to exit this window (servers will continue running)
pause >nul

