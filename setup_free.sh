#!/bin/bash
# Setup script voor GRATIS HuggingFace modellen

echo "========================================"
echo "Benjamin AI Agent - GRATIS Setup"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python niet gevonden!"
    exit 1
fi

echo "[1/3] Installing HuggingFace packages..."
pip3 install transformers torch requests

echo ""
echo "[2/3] Kies je gratis optie:"
echo ""
echo "1. HuggingFace Inference API (gratis tier, geen installatie nodig)"
echo "   - Snel en eenvoudig"
echo "   - Vereist gratis API key van https://huggingface.co/settings/tokens"
echo ""
echo "2. Lokaal model (volledig gratis, maar langzamer)"
echo "   - Geen internet nodig na download"
echo "   - Vereist ~8GB RAM en GPU aanbevolen"
echo ""
read -p "Kies optie (1 of 2): " CHOICE

if [ "$CHOICE" = "1" ]; then
    echo ""
    echo "[3/3] HuggingFace API Key setup"
    echo ""
    echo "1. Ga naar: https://huggingface.co/settings/tokens"
    echo "2. Maak een account (gratis)"
    echo "3. Maak een nieuwe token (read access is genoeg)"
    echo "4. Kopieer de token"
    echo ""
    read -p "Plak je HuggingFace token hier: " HF_KEY
    
    if [ -n "$HF_KEY" ]; then
        SHELL_CONFIG=""
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_CONFIG="$HOME/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            SHELL_CONFIG="$HOME/.bashrc"
        fi
        
        if [ -n "$SHELL_CONFIG" ]; then
            echo "" >> "$SHELL_CONFIG"
            echo "# Benjamin AI Agent - HuggingFace API Key" >> "$SHELL_CONFIG"
            echo "export HUGGINGFACE_API_KEY=\"$HF_KEY\"" >> "$SHELL_CONFIG"
            echo "✅ Toegevoegd aan $SHELL_CONFIG"
        else
            echo "export HUGGINGFACE_API_KEY=\"$HF_KEY\"" >> "$HOME/.bash_profile"
            echo "✅ Toegevoegd aan ~/.bash_profile"
        fi
        
        export HUGGINGFACE_API_KEY="$HF_KEY"
        echo ""
        echo "✅ API key ingesteld!"
        echo ""
        echo "Je kunt nu Benjamin starten met:"
        echo "  python3 benjamin.py"
        echo ""
        echo "Het gebruikt standaard: mistralai/Mistral-7B-Instruct-v0.2"
    fi
elif [ "$CHOICE" = "2" ]; then
    echo ""
    echo "[3/3] Lokaal model setup"
    echo ""
    echo "Het model wordt automatisch gedownload bij eerste gebruik."
    echo "Dit kan 5-15 minuten duren en ~15GB ruimte kosten."
    echo ""
    echo "Standaard model: mistralai/Mistral-7B-Instruct-v0.2"
    echo ""
    echo "Je kunt nu Benjamin starten met:"
    echo "  python3 benjamin.py"
    echo ""
    echo "Het model wordt automatisch gedownload bij eerste run."
fi

echo ""
echo "✅ Setup compleet!"
echo ""
