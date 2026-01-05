@echo off
REM AI Visibility Tracker - Quick Start Script for Windows

echo ============================================================
echo AI VISIBILITY TRACKER - STARTING SERVER
echo ============================================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file from .env.example and add your API keys:
    echo   1. Copy .env.example to .env
    echo   2. Add your OpenAI API key
    echo   3. Add your Claude API key (optional)
    echo   4. Add your Gemini API key (optional)
    echo.
    pause
    exit /b 1
)

echo [1/3] Activating Anaconda environment...
call C:/Users/swast/anaconda3/Scripts/activate.bat
echo.

echo [2/3] Verifying setup...
python verify_setup.py
echo.

echo [3/3] Starting Django development server...
echo.
echo Server will start at: http://localhost:8000/
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python manage.py runserver

pause
