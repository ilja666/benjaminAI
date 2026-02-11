@echo off
REM Script om HuggingFace cache naar C:/ te zetten
echo ========================================
echo HuggingFace Cache naar C:/ Schijf
echo ========================================
echo.

REM Maak cache directory aan
if not exist "C:\huggingface_cache" (
    mkdir "C:\huggingface_cache"
    echo ✅ Cache directory aangemaakt: C:\huggingface_cache
) else (
    echo ✅ Cache directory bestaat al: C:\huggingface_cache
)

REM Zet environment variables voor deze sessie
setx HF_HOME "C:\huggingface_cache" >nul 2>&1
setx HUGGINGFACE_HUB_CACHE "C:\huggingface_cache" >nul 2>&1
set HF_HOME=C:\huggingface_cache
set HUGGINGFACE_HUB_CACHE=C:\huggingface_cache

echo.
echo ✅ Environment variables ingesteld!
echo.
echo Cache locatie: C:\huggingface_cache
echo.
echo Je kunt nu Benjamin starten:
echo   python benjamin.py
echo.
echo Modellen worden nu opgeslagen op C:/ schijf
echo.
pause
