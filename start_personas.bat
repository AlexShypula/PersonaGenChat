@echo off
title Persona System Launcher
echo.
echo 🎭 Starting Persona System...
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check for .env file
if not exist ".env" (
    echo ⚠️  No .env file found!
    echo You need to create a .env file with your OpenAI API key
    echo.
    set /p api_key="Enter your OpenAI API key: "
    echo OPENAI_API_KEY=!api_key! > .env
    echo ✅ .env file created!
    echo.
)

REM Change to frontend directory
cd frontend

REM Install requirements
echo 📦 Installing/checking requirements...
pip install -r requirements.txt >nul 2>&1

REM Start the application
echo 🚀 Starting web interface...
echo 📱 Your browser should open automatically
echo 🌐 If not, go to: http://localhost:8501
echo.
echo 💡 To stop the server, close this window
echo ================================
echo.

start "" "http://localhost:8501"
python -m streamlit run app.py --server.port 8501

pause
