#!/bin/bash
# Benjamin AI Agent - Start Script (Linux/Mac)

echo "========================================"
echo "Benjamin AI Agent"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python niet gevonden!"
    echo "Installeer Python van https://www.python.org"
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."
if ! pip3 show openai &> /dev/null; then
    echo "OpenAI niet gevonden. Installeren..."
    pip3 install openai
fi

# Check API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY niet gevonden!"
    echo ""
    echo "Zet je API key met:"
    echo "  export OPENAI_API_KEY=\"sk-jouw-key-hier\""
    echo ""
    echo "Of run eerst: ./setup_gpt4.sh"
    echo ""
    exit 1
fi

# Start interactive mode
echo ""
echo "Starting Benjamin in interactive mode..."
echo "(Gebruik 'quit' om te stoppen)"
echo ""
python3 benjamin.py interactive
