@echo off
REM Setup script voor GPT-4
echo ========================================
echo Benjamin AI Agent - GPT-4 Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python niet gevonden!
    pause
    exit /b 1
)

echo [1/2] Installing OpenAI package...
pip install openai>=1.0.0

echo.
echo [2/2] API Key setup
echo.
echo Je hebt een OpenAI API key nodig om GPT-4 te gebruiken.
echo.
echo 1. Ga naar: https://platform.openai.com/api-keys
echo 2. Maak een nieuwe API key aan
echo 3. Kopieer de key (begint met sk-...)
echo.
set /p API_KEY="Plak je API key hier: "

if "%API_KEY%"=="" (
    echo Geen key ingevoerd. Setup gestopt.
    pause
    exit /b 1
)

REM Set environment variable voor deze sessie
setx OPENAI_API_KEY "%API_KEY%" >nul 2>&1
set OPENAI_API_KEY=%API_KEY%

echo.
echo ✅ API key ingesteld!
echo.
echo Je kunt nu Benjamin starten met:
echo   python benjamin.py
echo.
echo Of gebruik: start_benjamin.bat
echo.
pause
