@echo off
echo ========================================
echo Cutting Process Feedback - Frontend Server
echo ========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js and add it to your PATH
    pause
    exit /b 1
)

cd frontend

REM Check if package.json exists
if not exist package.json (
    echo ERROR: package.json not found
    pause
    exit /b 1
)

REM Check if node_modules exists
if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting React frontend server...
echo Frontend will be available at http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

call npm start

pause



