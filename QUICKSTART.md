# Quick Start Guide

## Snelle Start (5 minuten)

### Stap 1: Installeer OpenAI Package

```bash
pip install openai
```

### Stap 2: Zet je API Key

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-jouw-api-key-hier"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-jouw-api-key-hier"
```

**Of gebruik het setup script:**
- Windows: `setup_gpt4.bat`
- Linux/Mac: `chmod +x setup_gpt4.sh && ./setup_gpt4.sh`

**API Key krijgen:**
1. Ga naar: https://platform.openai.com/api-keys
2. Maak een account en nieuwe key
3. Kopieer de key (begint met `sk-...`)

### Stap 3: Start Benjamin

**Windows:**
```bash
python benjamin.py
# Of dubbelklik op start_benjamin.bat
```

**Linux/Mac:**
```bash
python3 benjamin.py
# Of:
chmod +x start_benjamin.sh
./start_benjamin.sh
```

### Stap 4: Chat met Benjamin!

```
[08:00] Jij: Hoi Benjamin!
Benjamin: Hoi! Ik ben Benjamin...

[08:00] Jij: Hoe gaat het?
Benjamin: Goed! Ik was net wakker geworden...
```

## Eerste Commando's

- `status` - Zie hoe het met Benjamin gaat
- `reflect` - Laat hem nadenken over zichzelf
- `tick` - Versnel tijd met 1 uur
- `quit` - Stop en sla op

## Troubleshooting

**"OPENAI_API_KEY niet gevonden"**
- Zet je API key: `$env:OPENAI_API_KEY="sk-..."` (Windows) of `export OPENAI_API_KEY="sk-..."` (Linux/Mac)
- Of run: `setup_gpt4.bat` / `./setup_gpt4.sh`

**"Module not found"**
- Installeer: `pip install openai`

**"API error" / Rate limits**
- Check of je OpenAI account credits heeft
- Probeer `gpt-3.5-turbo` (goedkoper): `python benjamin.py interactive openai gpt-3.5-turbo`

**Alternatief: Ollama (gratis, lokaal)**
- Installeer: https://ollama.ai
- Download model: `ollama pull llama3.2`
- Start: `python benjamin.py interactive ollama llama3.2`

## Volgende Stappen

1. Laat Benjamin een dag leven: `python benjamin.py lifecycle`
2. Bekijk zijn geheugens in `benjamin_state_memories.json`
3. Experimenteer met verschillende LLM modellen
4. Pas zijn persoonlijkheid aan in de code

Veel plezier met Benjamin! 🚀
