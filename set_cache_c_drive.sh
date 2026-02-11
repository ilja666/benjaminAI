#!/bin/bash
# Script om HuggingFace cache naar C:/ te zetten (of andere locatie)

echo "========================================"
echo "HuggingFace Cache Configuratie"
echo "========================================"
echo ""

# Voor Linux/Mac gebruikers - vraag naar locatie
read -p "Waar wil je de cache? (default: ~/huggingface_cache): " CACHE_DIR
CACHE_DIR=${CACHE_DIR:-~/huggingface_cache}

# Maak directory aan
mkdir -p "$CACHE_DIR"
echo "✅ Cache directory: $CACHE_DIR"

# Zet environment variables
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if [ -n "$SHELL_CONFIG" ]; then
    echo "" >> "$SHELL_CONFIG"
    echo "# HuggingFace Cache Directory" >> "$SHELL_CONFIG"
    echo "export HF_HOME=\"$CACHE_DIR\"" >> "$SHELL_CONFIG"
    echo "export HUGGINGFACE_HUB_CACHE=\"$CACHE_DIR\"" >> "$SHELL_CONFIG"
    echo "✅ Toegevoegd aan $SHELL_CONFIG"
else
    echo "export HF_HOME=\"$CACHE_DIR\"" >> "$HOME/.bash_profile"
    echo "export HUGGINGFACE_HUB_CACHE=\"$CACHE_DIR\"" >> "$HOME/.bash_profile"
    echo "✅ Toegevoegd aan ~/.bash_profile"
fi

export HF_HOME="$CACHE_DIR"
export HUGGINGFACE_HUB_CACHE="$CACHE_DIR"

echo ""
echo "✅ Cache geconfigureerd!"
echo ""
echo "Start een nieuwe terminal of run:"
echo "  source $SHELL_CONFIG"
echo ""
echo "Dan start Benjamin:"
echo "  python3 benjamin.py"
echo ""
