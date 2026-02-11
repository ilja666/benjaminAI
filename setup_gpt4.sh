#!/bin/bash
# Setup script voor GPT-4

echo "========================================"
echo "Benjamin AI Agent - GPT-4 Setup"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python niet gevonden!"
    exit 1
fi

echo "[1/2] Installing OpenAI package..."
pip3 install openai>=1.0.0

echo ""
echo "[2/2] API Key setup"
echo ""
echo "Je hebt een OpenAI API key nodig om GPT-4 te gebruiken."
echo ""
echo "1. Ga naar: https://platform.openai.com/api-keys"
echo "2. Maak een nieuwe API key aan"
echo "3. Kopieer de key (begint met sk-...)"
echo ""
read -p "Plak je API key hier: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "Geen key ingevoerd. Setup gestopt."
    exit 1
fi

# Add to .bashrc/.zshrc
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if [ -n "$SHELL_CONFIG" ]; then
    echo "" >> "$SHELL_CONFIG"
    echo "# Benjamin AI Agent - OpenAI API Key" >> "$SHELL_CONFIG"
    echo "export OPENAI_API_KEY=\"$API_KEY\"" >> "$SHELL_CONFIG"
    echo "✅ Toegevoegd aan $SHELL_CONFIG"
else
    echo "export OPENAI_API_KEY=\"$API_KEY\"" >> "$HOME/.bash_profile"
    echo "✅ Toegevoegd aan ~/.bash_profile"
fi

export OPENAI_API_KEY="$API_KEY"

echo ""
echo "✅ API key ingesteld!"
echo ""
echo "Je kunt nu Benjamin starten met:"
echo "  python3 benjamin.py"
echo ""
echo "Of gebruik: ./start_benjamin.sh"
echo ""
