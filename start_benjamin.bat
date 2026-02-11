@echo off
REM Benjamin AI Agent - Start Script (Windows)
echo ========================================
echo Benjamin AI Agent
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python niet gevonden!
    echo Installeer Python van https://www.python.org
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
pip show openai >nul 2>&1
if errorlevel 1 (
    echo OpenAI niet gevonden. Installeren...
    pip install openai
)

REM Check API key
if "%OPENAI_API_KEY%"=="" (
    echo.
    echo ⚠️  OPENAI_API_KEY niet gevonden!
    echo.
    echo Zet je API key met:
    echo   $env:OPENAI_API_KEY="sk-jouw-key-hier"
    echo.
    echo Of run eerst: setup_gpt4.bat
    echo.
    pause
    exit /b 1
)

REM Start interactive mode
echo.
echo Starting Benjamin in interactive mode...
echo (Gebruik 'quit' om te stoppen)
echo.
python benjamin.py interactive

pause
