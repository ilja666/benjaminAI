# Gratis LLM Modellen voor Benjamin

Benjamin ondersteunt nu **volledig gratis** LLM's via HuggingFace! Geen API kosten meer.

## Opties

### 1. HuggingFace Inference API (Aanbevolen - Snel & Gratis)

**Voordelen:**
- ✅ Volledig gratis (gratis tier)
- ✅ Snel (geen lokale download)
- ✅ Geen GPU nodig
- ✅ Werkt op elke computer

**Setup:**
1. Maak gratis account: https://huggingface.co/join
2. Maak API token: https://huggingface.co/settings/tokens
3. Zet token:
   ```bash
   # Windows
   $env:HUGGINGFACE_API_KEY="hf_jouw-token-hier"
   
   # Linux/Mac
   export HUGGINGFACE_API_KEY="hf_jouw-token-hier"
   ```
4. Start Benjamin: `python benjamin.py`

**Gratis limieten:**
- 1000 requests per maand (gratis tier)
- Meestal genoeg voor persoonlijk gebruik

### 2. Lokaal HuggingFace Model (Volledig Gratis & Offline)

**Voordelen:**
- ✅ Volledig gratis
- ✅ Geen internet nodig (na download)
- ✅ Geen API limieten
- ✅ Volledige privacy

**Nadelen:**
- ⚠️ Eerste download: 5-15 minuten, ~15GB
- ⚠️ Vereist ~8GB RAM (16GB aanbevolen)
- ⚠️ Langzamer zonder GPU

**Setup:**
```bash
pip install transformers torch
python benjamin.py
# Model wordt automatisch gedownload bij eerste gebruik
```

**Aanbevolen modellen:**

| Model | Grootte | RAM nodig | Kwaliteit |
|-------|---------|-----------|-----------|
| `mistralai/Mistral-7B-Instruct-v0.2` | ~15GB | 8GB+ | ⭐⭐⭐⭐⭐ |
| `meta-llama/Llama-2-7b-chat-hf` | ~14GB | 8GB+ | ⭐⭐⭐⭐ |
| `microsoft/DialoGPT-medium` | ~350MB | 2GB+ | ⭐⭐⭐ |

**Voor GPU (veel sneller):**
- NVIDIA GPU met CUDA aanbevolen
- Automatisch gedetecteerd als beschikbaar

### 3. Ollama (Lokaal, Gratis)

**Voordelen:**
- ✅ Volledig gratis
- ✅ Eenvoudige installatie
- ✅ Goede performance

**Setup:**
```bash
# Installeer Ollama: https://ollama.ai
ollama pull llama3.2
python benjamin.py interactive ollama llama3.2
```

## Vergelijking

| Optie | Kosten | Snelheid | Setup | Offline |
|-------|-------|----------|-------|---------|
| HuggingFace API | Gratis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| Lokaal HF Model | Gratis | ⭐⭐⭐ | ⭐⭐⭐ | ✅ |
| Ollama | Gratis | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ |
| OpenAI GPT-4 | Betaald | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ |

## Aanbeveling

**Voor beginners:** HuggingFace Inference API
- Snelste setup
- Geen downloads
- Werkt meteen

**Voor privacy/offline:** Lokaal model
- Volledig offline
- Geen API limieten
- Volledige controle

**Voor beste performance:** Ollama
- Goede balans
- Eenvoudig te gebruiken
- Goede kwaliteit

## Model Kwaliteit

Alle gratis modellen zijn goed genoeg voor Benjamin:
- ✅ Natuurlijke gesprekken
- ✅ Goede Nederlandse taal
- ✅ Begrijpt context
- ✅ Puberale persoonlijkheid

GPT-4 is beter, maar de gratis alternatieven zijn zeker goed genoeg voor dit project!

## Troubleshooting

**"Model laadt niet"**
- Check internet verbinding (voor download)
- Check beschikbare schijfruimte (~15GB)
- Probeer kleiner model

**"Out of memory"**
- Gebruik Inference API in plaats van lokaal
- Of gebruik kleiner model
- Sluit andere programma's

**"API rate limit"**
- Gratis tier heeft limieten
- Wacht even of upgrade account
- Of gebruik lokaal model

## Starten

```bash
# Gratis (standaard)
python benjamin.py

# Met specifiek model
python benjamin.py interactive huggingface mistralai/Mistral-7B-Instruct-v0.2

# Ollama
python benjamin.py interactive ollama llama3.2
```

Veel plezier met gratis Benjamin! 🎉
