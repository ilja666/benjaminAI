@echo off
REM Setup script voor GRATIS HuggingFace modellen
echo ========================================
echo Benjamin AI Agent - GRATIS Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python niet gevonden!
    pause
    exit /b 1
)

echo [1/3] Installing HuggingFace packages...
pip install transformers torch requests

echo.
echo [2/3] Kies je gratis optie:
echo.
echo 1. HuggingFace Inference API (gratis tier, geen installatie nodig)
echo    - Snel en eenvoudig
echo    - Vereist gratis API key van https://huggingface.co/settings/tokens
echo.
echo 2. Lokaal model (volledig gratis, maar langzamer)
echo    - Geen internet nodig na download
echo    - Vereist ~8GB RAM en GPU aanbevolen
echo.
set /p CHOICE="Kies optie (1 of 2): "

if "%CHOICE%"=="1" (
    echo.
    echo [3/3] HuggingFace API Key setup
    echo.
    echo 1. Ga naar: https://huggingface.co/settings/tokens
    echo 2. Maak een account (gratis)
    echo 3. Maak een nieuwe token (read access is genoeg)
    echo 4. Kopieer de token
    echo.
    set /p HF_KEY="Plak je HuggingFace token hier: "
    
    if not "%HF_KEY%"=="" (
        setx HUGGINGFACE_API_KEY "%HF_KEY%" >nul 2>&1
        set HUGGINGFACE_API_KEY=%HF_KEY%
        echo.
        echo ✅ API key ingesteld!
        echo.
        echo Je kunt nu Benjamin starten met:
        echo   python benjamin.py
        echo.
        echo Het gebruikt standaard: mistralai/Mistral-7B-Instruct-v0.2
    )
) else if "%CHOICE%"=="2" (
    echo.
    echo [3/3] Lokaal model setup
    echo.
    echo Het model wordt automatisch gedownload bij eerste gebruik.
    echo Dit kan 5-15 minuten duren en ~15GB ruimte kosten.
    echo.
    echo Standaard model: mistralai/Mistral-7B-Instruct-v0.2
    echo.
    echo Je kunt nu Benjamin starten met:
    echo   python benjamin.py
    echo.
    echo Het model wordt automatisch gedownload bij eerste run.
)

echo.
echo ✅ Setup compleet!
echo.
pause
