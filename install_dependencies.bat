@echo off
echo ========================================
echo Installing All Dependencies
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
) else (
    python --version
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
) else (
    node --version
)

echo.
echo [1/2] Installing backend dependencies...
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
echo Backend dependencies installed successfully.
echo.

echo [2/2] Installing frontend dependencies...
cd ..\frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
echo Frontend dependencies installed successfully.
echo.

cd ..
echo ========================================
echo All dependencies installed successfully!
echo ========================================
echo.
echo You can now run:
echo - run_app.bat (to run both servers)
echo - run_backend.bat (to run only backend)
echo - run_frontend.bat (to run only frontend)
echo.
pause

