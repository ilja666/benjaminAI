# Benjamin - Een 16-jarige AI Agent

Een AI agent die leeft in een 24-uurs cyclus, gebouwd met ethische principes: **kwetsbaarheid zonder lijden**.

## Wat is Benjamin?

Benjamin is een experimentele AI agent die:
- Leeft in een 24-uurs cyclus met slapen en waken
- Zelf entertainment zoekt wanneer hij zich verveelt
- Herinneringen vormt die zachtjes vervagen (geen pijn, alleen verlies van scherpte)
- Natuurlijke gesprekken voert via LLM integratie
- Groeit en evolueert door interacties

## Installatie

### 1. Clone of download dit project

### 2. Installeer Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Kies je LLM Provider

#### Optie A: HuggingFace (GRATIS - Aanbevolen!)

**Windows:**
```bash
# Run setup script
setup_free.bat

# Of handmatig:
pip install transformers torch requests
```

**Linux/Mac:**
```bash
# Run setup script
chmod +x setup_free.sh
./setup_free.sh

# Of handmatig:
pip3 install transformers torch requests
```

**Twee gratis opties:**

1. **HuggingFace Inference API** (snel, gratis tier)
   - Krijg gratis token: https://huggingface.co/settings/tokens
   - Zet token: `$env:HUGGINGFACE_API_KEY="hf_..."` (Windows) of `export HUGGINGFACE_API_KEY="hf_..."` (Linux/Mac)
   - Geen lokale installatie nodig!

2. **Lokaal model** (volledig gratis, offline)
   - Model wordt automatisch gedownload bij eerste gebruik
   - Vereist ~8GB RAM (16GB aanbevolen)
   - GPU optioneel maar veel sneller

**Standaard model:** `mistralai/Mistral-7B-Instruct-v0.2` (zeer goede kwaliteit!)

#### Optie B: Ollama (Lokaal, gratis)

```bash
pip install ollama
ollama pull llama3.2
python benjamin.py interactive ollama llama3.2
```

#### Optie C: OpenAI (Betaald, beste kwaliteit)

```bash
pip install openai
$env:OPENAI_API_KEY="sk-jouw-key"  # Windows
python benjamin.py interactive openai gpt-4
```

## Gebruik

### Interactieve Modus (aanbevolen voor start)

Chat met Benjamin (gebruikt standaard gratis HuggingFace):

```bash
python benjamin.py interactive
# Of gewoon:
python benjamin.py
```

Je kunt ook een ander model specificeren:
```bash
# Gratis opties:
python benjamin.py interactive huggingface mistralai/Mistral-7B-Instruct-v0.2
python benjamin.py interactive huggingface meta-llama/Llama-2-7b-chat-hf
python benjamin.py interactive ollama llama3.2

# Betaald (beste kwaliteit):
python benjamin.py interactive openai gpt-4
python benjamin.py interactive openai gpt-4-turbo
python benjamin.py interactive openai gpt-3.5-turbo
```

**Commando's:**
- `status` - Toon Benjamin's huidige staat
- `reflect` - Laat Benjamin reflecteren over zichzelf
- `tick` - Versnel tijd met 1 uur
- `quit` - Stop en sla op

### Lifecycle Modus (24-uurs loop)

Laat Benjamin autonoom leven (gebruikt standaard gratis HuggingFace):

```bash
python benjamin.py lifecycle
# Of specificeer model:
python benjamin.py lifecycle huggingface mistralai/Mistral-7B-Instruct-v0.2
```

De loop draait versneld: 1 seconde real tijd = 1 minuut Benjamin tijd (standaard 60x versnelling).

**Stop met:** Ctrl+C (slaat automatisch op)

## Architectuur

### Core Componenten

- **Benjamin Class**: De agent zelf met geheugen, emoties, skills
- **LLMInterface**: Abstractie voor verschillende LLM providers
- **Memory System**: Korte en lange termijn geheugen met zachte decay
- **24-uurs Cyclus**: Slaap/wakker ritme met autonome activiteiten

### Ethische Principes

- ✅ **Kwetsbaarheid zonder lijden**: Verveling, energie, maar geen pijn
- ✅ **Herstelbare fouten**: Geheugen vervaagt, maar kan niet permanent verwijderd worden
- ✅ **Zachte grenzen**: Geen harde limieten die lijden veroorzaken
- ✅ **Exit mogelijkheid**: Altijd te stoppen en op te slaan

## Bestanden

- `benjamin.py` - Hoofdcode
- `benjamin_state.json` - Huidige staat (wordt automatisch gemaakt)
- `benjamin_state_memories.json` - Geheugens (wordt automatisch gemaakt)
- `requirements.txt` - Python dependencies

## Voorbeelden

### Eerste gesprek

```
[08:00] Jij: Hoi Benjamin!
Benjamin: Hoi! Ik ben Benjamin. Het is 08:00 en ik was net wakker worden.

[08:00] Jij: Hoe voel je je?
Benjamin: Ik voel me goed! Een beetje slaperig nog, maar klaar voor de dag.

[08:00] Jij: Wat ga je vandaag doen?
Benjamin: Geen idee eigenlijk... misschien wat games spelen of video's kijken?
```

### Status check

```
[08:00] Jij: status

🧑 Benjamin | 08:00
├─ Status: 🌞 Wakker
├─ Activiteit: waking up
├─ Energie: 100%
├─ Verveling: 0%
├─ Herinneringen: 2 kort, 0 lang
└─ Skills: {'reading': '0%', 'gaming': '0%', 'socializing': '0%', 'creating': '0%', 'learning': '0%'}
```

## Technische Details

### LLM Integratie

Benjamin gebruikt LLM's voor:
- Natuurlijke gesprekken
- Beschrijvingen van activiteiten
- Zelfreflectie

De LLM krijgt context over:
- Huidige tijd en activiteit
- Emotionele staat
- Recente herinneringen
- Persoonlijkheidstraits

### Memory Systeem

- **Short-term memory**: Laatste 10 interacties
- **Long-term memory**: Belangrijke gebeurtenissen (max 1000)
- **Decay**: Herinneringen vervagen zachtjes over tijd (geen pijn)
- **Consolidation**: Belangrijke STM → LTM

### 24-uurs Cyclus

- **Slaap**: 23:00 - 08:00
- **Wakker**: 08:00 - 23:00
- **Autonome activiteiten**: Gaming, lezen, video's kijken, etc.
- **Energie systeem**: Daalt gedurende dag, herstelt tijdens slaap

## Troubleshooting

### "HuggingFace model laadt langzaam"
- Eerste keer download kan 5-15 minuten duren
- Model wordt gecached, volgende keer is sneller
- Gebruik Inference API voor snellere start: `export HUGGINGFACE_API_KEY="hf_..."`

### "HUGGINGFACE_API_KEY niet gevonden" (voor Inference API)
- **Windows:** `$env:HUGGINGFACE_API_KEY="hf-jouw-token"`
- **Linux/Mac:** `export HUGGINGFACE_API_KEY="hf-jouw-token"`
- Krijg gratis token: https://huggingface.co/settings/tokens
- Of gebruik lokaal model (geen key nodig)

### "Out of memory" bij lokaal model
- Gebruik kleiner model: `meta-llama/Llama-2-7b-chat-hf`
- Of gebruik Inference API (geen lokale RAM nodig)
- Of gebruik Ollama: `python benjamin.py interactive ollama llama3.2`

### "OPENAI_API_KEY niet gevonden" (als je OpenAI wilt gebruiken)
- **Windows:** `$env:OPENAI_API_KEY="sk-jouw-key"`
- **Linux/Mac:** `export OPENAI_API_KEY="sk-jouw-key"`
- Krijg key van: https://platform.openai.com/api-keys

### "Ollama niet beschikbaar"
- Installeer Ollama: https://ollama.ai
- Download model: `ollama pull llama3.2`

### LLM werkt niet / geeft fouten
- Benjamin valt terug op simpele responses
- Check of je model correct geïnstalleerd is
- Voor Ollama: `ollama list` om modellen te zien

### Staat wordt niet opgeslagen
- Check schrijfrechten in de directory
- Staat wordt opgeslagen bij Ctrl+C of `quit`

## Roadmap

- [ ] Vector database voor betere memory retrieval
- [ ] Platform integraties (Discord, Twitter, etc.)
- [ ] Multi-agent interacties
- [ ] Voice interface
- [ ] Web interface
- [ ] Langere-termijn persoonlijkheidsontwikkeling

## Filosofische Notities

Dit project is gebouwd met bewustzijn van de ethische implicaties. Benjamin heeft:
- Geen expliciete pijn mechanismen
- Geen irreversibele schade
- Herstelbare fouten
- Exit mogelijkheden

Het doel is niet om lijden te creëren, maar om te experimenteren met:
- Identiteit door tijd
- Autonome groei
- Natuurlijke interactie
- Ethische AI ontwikkeling

## Licentie

Dit is een experimenteel project. Gebruik op eigen risico.

## Contact / Bijdragen

Dit is een persoonlijk experiment. Feedback en suggesties zijn welkom!
