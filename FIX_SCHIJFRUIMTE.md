# Fix: Geen Schijfruimte voor Lokaal Model

## Probleem
Het lokale HuggingFace model heeft ~15GB schijfruimte nodig. Als je niet genoeg ruimte hebt, krijg je een fout.

## Oplossingen

### Optie 1: Gebruik Inference API (Aanbevolen - Geen Download!)

**Stap 1:** Krijg gratis HuggingFace token
1. Ga naar: https://huggingface.co/join (maak account)
2. Ga naar: https://huggingface.co/settings/tokens
3. Maak nieuwe token (read access is genoeg)
4. Kopieer token (begint met `hf_...`)

**Stap 2:** Zet token
```powershell
# Windows PowerShell
$env:HUGGINGFACE_API_KEY="hf_jouw-token-hier"

# Windows CMD
set HUGGINGFACE_API_KEY=hf_jouw-token-hier

# Linux/Mac
export HUGGINGFACE_API_KEY="hf_jouw-token-hier"
```

**Stap 3:** Start Benjamin
```bash
python benjamin.py
```

Nu gebruikt Benjamin de Inference API - geen download nodig!

### Optie 2: Maak Schijfruimte Vrij

Als je toch lokaal wilt draaien:
1. Verwijder oude downloads uit `C:\Users\Ilja\.cache\huggingface\`
2. Of gebruik een andere schijf met meer ruimte
3. Je hebt minimaal ~15GB nodig

### Optie 3: Gebruik Kleiner Model

Kleinere modellen die minder ruimte nodig hebben:

```bash
# Veel kleiner (~350MB)
python benjamin.py interactive huggingface microsoft/DialoGPT-medium

# Middelgroot (~1-2GB)
python benjamin.py interactive huggingface gpt2
```

### Optie 4: Gebruik Ollama (Lokaal, maar anders)

```bash
# Installeer Ollama: https://ollama.ai
ollama pull llama3.2
python benjamin.py interactive ollama llama3.2
```

## Automatische Fallback

De code probeert nu automatisch naar Inference API te switchen als er geen schijfruimte is - maar je moet wel een API key hebben!

## Check Schijfruimte

**Windows:**
```powershell
Get-PSDrive C | Select-Object Used,Free
```

**Linux/Mac:**
```bash
df -h
```

Je hebt minimaal 15GB vrij nodig voor het standaard model.
