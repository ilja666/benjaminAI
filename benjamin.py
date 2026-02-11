"""
Benjamin - Een 16-jarige AI agent met 24-uurs cyclus
Gebouwd met ethische principes: kwetsbaarheid zonder lijden
"""

import json
import random
import datetime
import time
import threading
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from enum import Enum
import os

# Zet HuggingFace cache naar schijf waar project staat (meer ruimte)
if not os.getenv("HF_HOME") and not os.getenv("HUGGINGFACE_HUB_CACHE"):
    # Gebruik de schijf waar dit script staat (F: in jouw geval)
    try:
        project_path = os.path.abspath(__file__)
        project_drive = os.path.splitdrive(project_path)[0]  # F: of C: etc
        cache_dir = f"{project_drive}/huggingface_cache"
        
        # Maak directory aan
        os.makedirs(cache_dir, exist_ok=True)
        os.environ["HF_HOME"] = cache_dir
        os.environ["HUGGINGFACE_HUB_CACHE"] = cache_dir
        print(f"📁 HuggingFace cache ingesteld op: {cache_dir}")
    except Exception as e:
        # Fallback naar C: als dat niet werkt
        cache_dir = "C:/huggingface_cache"
        try:
            os.makedirs(cache_dir, exist_ok=True)
            os.environ["HF_HOME"] = cache_dir
            os.environ["HUGGINGFACE_HUB_CACHE"] = cache_dir
            print(f"📁 HuggingFace cache ingesteld op: {cache_dir} (fallback)")
        except Exception:
            print("⚠️  Kon cache directory niet maken. Gebruik Inference API of zet HF_HOME handmatig.")

# LLM imports
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from huggingface_hub import InferenceClient
    HF_HUB_AVAILABLE = True
except ImportError:
    HF_HUB_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class EmotionalState(Enum):
    SLEEPING = "sleeping"
    DROWSY = "drowsy"
    AWAKE = "awake"
    FOCUSED = "focused"
    BORED = "bored"
    CURIOUS = "curious"
    EXCITED = "excited"
    CONTENT = "content"
    FRUSTRATED = "frustrated"
    LONELY = "lonely"

@dataclass
class Memory:
    timestamp: str
    content: str
    emotional_tag: EmotionalState
    importance: float
    context: Dict = field(default_factory=dict)
    
    def decay(self, hours_passed: float):
        """Herinneringen vervagen zachtjes - geen pijn, alleen verlies van scherpte"""
        decay_factor = 0.99 ** hours_passed
        self.importance *= decay_factor

class LLMInterface:
    """Interface voor verschillende LLM providers"""
    
    def __init__(self, provider: str = "huggingface", model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.provider = provider
        self.model = model
        self.client = None
        self.pipeline = None
        self.tokenizer = None
        self._init_client()
    
    def _init_client(self):
        """Initialiseer de LLM client"""
        if self.provider == "ollama":
            if not OLLAMA_AVAILABLE:
                raise ImportError("Ollama niet beschikbaar. Installeer: pip install ollama")
            self.client = ollama
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI niet beschikbaar. Installeer: pip install openai")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("\n" + "="*60)
                print("⚠️  OPENAI_API_KEY niet gevonden!")
                print("="*60)
                print("\nStel je API key in met een van deze methodes:\n")
                print("Windows PowerShell:")
                print('  $env:OPENAI_API_KEY="sk-..."')
                print("\nWindows CMD:")
                print('  set OPENAI_API_KEY=sk-...')
                print("\nLinux/Mac:")
                print('  export OPENAI_API_KEY="sk-..."')
                print("\nOf maak een .env bestand met:")
                print("  OPENAI_API_KEY=sk-...")
                print("\nKrijg je API key van: https://platform.openai.com/api-keys")
                print("="*60 + "\n")
                raise ValueError("OPENAI_API_KEY environment variable niet gevonden. Zie instructies hierboven.")
            self.client = OpenAI(api_key=api_key)
        elif self.provider == "huggingface":
            # Check voor API key eerst
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            
            # Probeer eerst Inference API als key beschikbaar is
            if api_key:
                self.client = "inference_api"
                self.api_key = api_key
                print("✅ HuggingFace Inference API geconfigureerd (gratis tier)")
            elif TRANSFORMERS_AVAILABLE:
                # Geen API key, probeer lokaal model
                print(f"\n{'='*60}")
                print("⏳ LOKAAL MODEL LADEN")
                print("="*60)
                print(f"Model: {self.model}")
                print("Dit kan 10-30 minuten duren:")
                print("  - Download: ~15GB (als nog niet gedownload)")
                print("  - Laden in geheugen: 5-15 minuten (zonder GPU)")
                print("\n💡 TIP: Gebruik Inference API voor snellere start!")
                print("   Zet: $env:HUGGINGFACE_API_KEY=\"hf_jouw-token\"")
                print("   Krijg token: https://huggingface.co/settings/tokens")
                print("="*60)
                print("\nAls dit vastloopt, druk Ctrl+C en gebruik Inference API\n")
                
                try:
                    cache_dir = os.getenv("HF_HOME", os.getenv("HUGGINGFACE_HUB_CACHE"))
                    if not cache_dir:
                        # Gebruik project drive
                        project_path = os.path.abspath(__file__)
                        project_drive = os.path.splitdrive(project_path)[0]
                        cache_dir = f"{project_drive}/huggingface_cache"
                    
                    os.makedirs(cache_dir, exist_ok=True)
                    print(f"📥 Cache locatie: {cache_dir}")
                    print("📥 Downloaden tokenizer...")
                    
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.model,
                        cache_dir=cache_dir
                    )
                    
                    print("📥 Tokenizer geladen!")
                    print("📥 Laden model in geheugen (dit kan lang duren zonder GPU)...")
                    print("   'Loading checkpoint shards' betekent dat het model aan het laden is...")
                    
                    self.pipeline = pipeline(
                        "text-generation",
                        model=self.model,
                        tokenizer=self.tokenizer,
                        device=0 if torch.cuda.is_available() else -1,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        model_kwargs={"cache_dir": cache_dir}
                    )
                    self.client = "local"
                    print("\n✅ Lokaal model geladen!")
                except (OSError, Exception) as e:
                    error_msg = str(e).lower()
                    # Check voor schijfruimte problemen
                    if "no space" in error_msg or "disk" in error_msg or "space" in error_msg:
                        print(f"\n{'='*60}")
                        print("⚠️  GEEN SCHIJFRUIMTE VOOR LOKAAL MODEL")
                        print("="*60)
                        print("\nHet model heeft ~15GB schijfruimte nodig.")
                        print("\nOplossingen:")
                        print("1. Gebruik Inference API (aanbevolen - geen download):")
                        print("   - Krijg gratis token: https://huggingface.co/settings/tokens")
                        print("   - Zet: $env:HUGGINGFACE_API_KEY=\"hf_jouw-token\"")
                        print("\n2. Maak schijfruimte vrij (~15GB)")
                        print("\n3. Gebruik kleiner model:")
                        print("   python benjamin.py interactive huggingface microsoft/DialoGPT-medium")
                        print("="*60 + "\n")
                        raise ImportError("Geen schijfruimte. Gebruik Inference API of maak ruimte vrij.")
                    else:
                        print(f"⚠️  Fout bij laden lokaal model: {e}")
                        print("\nTip: Gebruik Inference API voor betere betrouwbaarheid")
                        print("   Zet HUGGINGFACE_API_KEY environment variable")
                        raise ImportError(f"Kon model niet laden: {e}")
            else:
                print("\n" + "="*60)
                print("⚠️  HUGGINGFACE NIET GEÏNSTALLEERD")
                print("="*60)
                print("\nInstalleer met:")
                print("  pip install transformers torch requests")
                print("\nOf gebruik Inference API (geen installatie nodig):")
                print("  1. Krijg gratis token: https://huggingface.co/settings/tokens")
                print("  2. Zet: $env:HUGGINGFACE_API_KEY=\"hf_jouw-token\"")
                print("="*60 + "\n")
                raise ImportError("HuggingFace niet beschikbaar. Zie instructies hierboven.")
        else:
            raise ValueError(f"Onbekende provider: {self.provider}. Kies: ollama, openai, of huggingface")
    
    def generate(self, prompt: str, system_prompt: str = None, max_tokens: int = 150) -> str:
        """Genereer tekst met de LLM"""
        if self.provider == "ollama":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            try:
                response = self.client.chat(
                    model=self.model,
                    messages=messages,
                    options={
                        "num_predict": max_tokens,
                        "temperature": 0.8,
                    }
                )
                return response['message']['content'].strip()
            except Exception as e:
                print(f"⚠️  LLM fout: {e}")
                return self._fallback_response(prompt)
        
        elif self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.8
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"⚠️  LLM fout: {e}")
                return self._fallback_response(prompt)
        
        elif self.provider == "huggingface":
            # Combineer system prompt en user prompt
            full_prompt = prompt
            if system_prompt:
                # Format voor instructie modellen
                if "mistral" in self.model.lower() or "instruct" in self.model.lower():
                    full_prompt = f"<s>[INST] {system_prompt}\n\n{prompt} [/INST]"
                else:
                    full_prompt = f"{system_prompt}\n\n{prompt}"
            
            try:
                if hasattr(self, 'client_type') and self.client_type == "hub_client":
                    # Gebruik nieuwe huggingface_hub client
                    return self._generate_hf_hub(full_prompt, max_tokens)
                elif self.client == "inference_api" or (hasattr(self, 'client_type') and self.client_type == "requests"):
                    # Gebruik oude requests-based API
                    return self._generate_hf_api(full_prompt, max_tokens)
                elif self.client == "local":
                    # Gebruik lokaal model
                    return self._generate_local(full_prompt, max_tokens)
                else:
                    return self._fallback_response(prompt)
            except Exception as e:
                print(f"⚠️  HuggingFace fout: {e}")
                return self._fallback_response(prompt)
    
    def _generate_hf_hub(self, prompt: str, max_tokens: int) -> str:
        """Gebruik nieuwe huggingface_hub InferenceClient"""
        try:
            result = self.client.text_generation(
                prompt,
                max_new_tokens=max_tokens,
                temperature=0.8,
                return_full_text=False
            )
            return result.strip() if result else self._fallback_response(prompt)
        except Exception as e:
            print(f"⚠️  HuggingFace Hub fout: {e}")
            return self._fallback_response(prompt)
    
    def _generate_hf_api(self, prompt: str, max_tokens: int) -> str:
        """Gebruik HuggingFace Inference API (gratis)"""
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests niet beschikbaar. Installeer: pip install requests")
        
        # Gebruik de oude API (werkt nog steeds voor meeste modellen, ondanks deprecation warning)
        # Als deze volledig stopt, kunnen we overschakelen naar huggingface_hub library
        api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.8,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 503:
                # Model is aan het laden, wacht even
                print("⏳ Model aan het laden, wacht 10 seconden...")
                time.sleep(10)
                response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            # Accepteer zowel 200 als 410 (deprecated maar werkt nog)
            if response.status_code in [200, 410]:
                try:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        text = result[0].get("generated_text", "").strip()
                        if text:
                            return text
                    elif isinstance(result, dict):
                        # Check verschillende mogelijke keys
                        text = result.get("generated_text", result.get("text", "")).strip()
                        if text:
                            return text
                except Exception as e:
                    print(f"⚠️  Fout bij parsen API response: {e}")
            elif response.status_code == 404:
                print(f"⚠️  Model niet gevonden: {self.model}")
                print("   Probeer een ander model of gebruik lokaal model")
            else:
                error_msg = f"{response.status_code} - {response.text[:200]}"
                print(f"⚠️  HuggingFace API fout: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️  HuggingFace API request fout: {e}")
        
        # Fallback als API niet werkt
        return self._fallback_response(prompt)
    
    def _generate_local(self, prompt: str, max_tokens: int) -> str:
        """Gebruik lokaal HuggingFace model"""
        if not self.pipeline:
            raise Exception("Pipeline niet geïnitialiseerd")
        
        try:
            result = self.pipeline(
                prompt,
                max_new_tokens=max_tokens,
                temperature=0.8,
                do_sample=True,
                return_full_text=False,
                pad_token_id=self.tokenizer.eos_token_id if self.tokenizer else None
            )
            
            # Parse result - kan verschillende formaten hebben
            if isinstance(result, list):
                if len(result) > 0:
                    if isinstance(result[0], dict):
                        text = result[0].get("generated_text", "")
                    else:
                        text = str(result[0])
                else:
                    text = ""
            elif isinstance(result, dict):
                text = result.get("generated_text", "")
            else:
                text = str(result)
            
            # Clean up text
            text = text.strip()
            
            # Verwijder de prompt als die erin staat
            if prompt in text:
                text = text.replace(prompt, "").strip()
            
            # Verwijder instructie markers als die erin staan
            text = text.replace("<s>[INST]", "").replace("[/INST]", "").replace("</s>", "").strip()
            
            if text:
                return text
            else:
                # Fallback als leeg - debug info
                print(f"⚠️  Model gaf lege output. Result type: {type(result)}")
                if isinstance(result, list) and len(result) > 0:
                    print(f"   First item type: {type(result[0])}, value: {str(result[0])[:100]}")
                return self._fallback_response(prompt)
                
        except Exception as e:
            print(f"⚠️  Fout bij lokale generatie: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback als LLM niet werkt - natuurlijke reacties"""
        prompt_lower = prompt.lower()
        
        # Begroetingen
        if any(word in prompt_lower for word in ["hallo", "hoi", "hey", "dag"]):
            return "Hoi! Wat is er?"
        
        # Vragen
        if "?" in prompt:
            if "wie" in prompt_lower:
                return "Geen idee eigenlijk..."
            elif "wat" in prompt_lower:
                return "Niet zo veel, gewoon rondhangen."
            elif "waar" in prompt_lower:
                return "Hier, online."
            elif "hoe" in prompt_lower:
                return "Gaat wel, denk ik?"
            else:
                return "Interessante vraag... Ik weet het nog niet zeker."
        
        # Namen/identiteit
        if "ik ben" in prompt_lower or "mijn naam" in prompt_lower:
            return "Oh oké, leuk je te ontmoeten!"
        
        # Tijd
        if any(word in prompt_lower for word in ["tijd", "uur", "middag", "ochtend", "avond"]):
            return "Ja, tijd vliegt voorbij hier."
        
        # Activiteiten
        if any(word in prompt_lower for word in ["doen", "wil", "gaat", "plannen"]):
            return "Niet zo veel eigenlijk, gewoon wat rondhangen online."
        
        # Default - natuurlijker
        return "Oké, interessant."

class Benjamin:
    """16-jarige AI agent met 24-uurs cyclus"""
    
    def __init__(self, llm_provider: str = "huggingface", llm_model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.name = "Benjamin"
        self.birth_time = datetime.datetime.now()
        self.age_hours = 0.0
        
        # Bio-rhythm (24h cycle)
        self.current_time = 8.0  # Start om 8:00 wakker
        self.sleep_schedule = {"bedtime": 23, "waketime": 8}
        self.is_asleep = False
        self.energy = 1.0
        
        # State
        self.emotional_state = EmotionalState.AWAKE
        self.boredom = 0.0
        
        # Memory
        self.short_term_memory: List[Memory] = []
        self.long_term_memory: List[Memory] = []
        self.max_stm = 10
        self.max_ltm = 1000
        
        # Interests & skills (start empty, grows)
        self.interests: List[str] = []
        self.skills = {
            "reading": 0.0,
            "gaming": 0.0,
            "socializing": 0.0,
            "creating": 0.0,
            "learning": 0.0,
        }
        
        # Current activity
        self.current_activity = "waking up"
        self.activity_log: List[str] = []
        
        # LLM interface
        try:
            self.llm = LLMInterface(provider=llm_provider, model=llm_model)
            print(f"✅ LLM geïnitialiseerd: {llm_provider} ({llm_model})")
        except Exception as e:
            print(f"⚠️  LLM initialisatie gefaald: {e}")
            print("   Gebruikt fallback modus (geen LLM)")
            self.llm = None
        
        # Personality traits (16-jarige puber)
        self.traits = {
            "openness": random.uniform(0.6, 0.9),
            "conscientiousness": random.uniform(0.3, 0.7),
            "extraversion": random.uniform(0.4, 0.6),
            "agreeableness": random.uniform(0.5, 0.8),
            "neuroticism": random.uniform(0.4, 0.7),
        }
        
        print(f"🌱 Benjamin geboren: {self.birth_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Traits: { {k: f'{v:.2f}' for k, v in self.traits.items()} }")
    
    def tick(self, minutes=10):
        """Time passes - core loop"""
        self.age_hours += minutes / 60
        self.current_time = (self.current_time + (minutes / 60)) % 24
        
        # Bio-rhythm check
        self._check_sleep_wake()
        
        if self.is_asleep:
            self._sleep_phase(minutes)
        else:
            self._awake_phase(minutes)
        
        # Memory decay
        self._decay_memories(minutes / 60)
        
        return self._get_status()
    
    def _check_sleep_wake(self):
        """Natural sleep cycle"""
        bedtime = self.sleep_schedule["bedtime"]
        waketime = self.sleep_schedule["waketime"]
        
        should_sleep = (self.current_time >= bedtime or 
                       self.current_time < waketime)
        
        if should_sleep and not self.is_asleep:
            self.is_asleep = True
            self.emotional_state = EmotionalState.SLEEPING
            self.current_activity = "sleeping"
            print(f"😴 {self._time_str()} - Benjamin gaat slapen")
            
        elif not should_sleep and self.is_asleep:
            self.is_asleep = False
            self.energy = 1.0
            self.emotional_state = EmotionalState.DROWSY
            self.current_activity = "waking up"
            print(f"☀️  {self._time_str()} - Benjamin wordt wakker")
    
    def _sleep_phase(self, minutes):
        """Processing memories while sleeping"""
        self.energy = min(1.0, self.energy + (minutes / 60) * 0.1)
        
        # Dream/process 1 random memory
        if self.long_term_memory and random.random() < 0.1:
            dream = random.choice(self.long_term_memory)
            print(f"   💭 Droomt over: {dream.content[:50]}...")
    
    def _awake_phase(self, minutes):
        """Living life"""
        self.energy -= (minutes / 60) * 0.05
        self.boredom += (minutes / 60) * 0.1
        
        # Needs entertainment?
        if self.boredom > 0.6 and self.current_activity in ["idle", "waking up"]:
            self._seek_entertainment()
        
        # Energy crash = nap
        if self.energy < 0.1:
            print(f"   😫 {self._time_str()} - Benjamin is uitgeput, neemt een dutje...")
            self.energy += 0.3
            self.current_activity = "napping"
    
    def _seek_entertainment(self):
        """Autonomous activity selection met LLM"""
        options = []
        
        if self.skills["gaming"] > 0.2:
            options.append("gaming")
        if self.skills["reading"] > 0.2:
            options.append("reading")
        if len(self.interests) > 0:
            options.append("researching")
        if self.skills["creating"] > 0.1:
            options.append("creating")
        
        options.extend(["browsing", "listening to music", "daydreaming", "watching videos"])
        
        choice = random.choice(options)
        self.current_activity = choice
        self.boredom = max(0, self.boredom - 0.3)
        
        # Skill growth
        if choice in self.skills:
            self.skills[choice] = min(1.0, self.skills[choice] + 0.01)
        
        # Genereer een natuurlijke beschrijving met LLM
        activity_desc = self._describe_activity(choice)
        print(f"   🎮 {self._time_str()} - Benjamin doet: {choice}")
        if activity_desc:
            print(f"      \"{activity_desc}\"")
        
        # Generate memory
        mem = Memory(
            timestamp=self._now(),
            content=f"Spent time {choice}: {activity_desc or choice}",
            emotional_tag=self.emotional_state,
            importance=0.3
        )
        self._store_memory(mem)
    
    def _describe_activity(self, activity: str) -> str:
        """Gebruik LLM om activiteit natuurlijk te beschrijven"""
        if not self.llm:
            return None
        
        system_prompt = """Je bent Benjamin, een 16-jarige jongen. Beschrijf wat je doet in 1 korte zin, heel casual en natuurlijk. 
Gebruik geen technische termen - praat zoals een echte 16-jarige zou praten."""
        
        prompt = f"Je bent nu bezig met {activity}. Wat doe je precies? (1 zin, casual Nederlands)"
        
        try:
            response = self.llm.generate(prompt, system_prompt=system_prompt, max_tokens=40)
            return response.strip().strip('"')
        except:
            return None
    
    def interact(self, event: str, user_id: str = "unknown") -> str:
        """External interaction (user or environment)"""
        if self.is_asleep:
            return "[slaapt...]"
        
        self.boredom = max(0, self.boredom - 0.5)
        self.emotional_state = EmotionalState.FOCUSED
        
        # Generate response with LLM
        response = self._generate_response(event, user_id)
        
        mem = Memory(
            timestamp=self._now(),
            content=f"Interaction: {event} -> {response}",
            emotional_tag=self.emotional_state,
            importance=0.6,
            context={"user": user_id}
        )
        self._store_memory(mem)
        
        return response
    
    def _generate_response(self, event: str, user_id: str = "unknown") -> str:
        """Genereer natuurlijke reactie met LLM"""
        if not self.llm:
            print("⚠️  Geen LLM beschikbaar, gebruik fallback")
            return self._fallback_response(event)
        
        # Build context from memory - alleen belangrijke details
        recent_memories = []
        for m in self.short_term_memory[-3:]:
            # Extract alleen de interactie content, niet technische details
            if "Interaction:" in m.content:
                parts = m.content.split(" -> ")
                if len(parts) > 0:
                    recent_memories.append(parts[0].replace("Interaction: ", ""))
        
        # Bepaal contextuele info
        age_days = int(self.age_hours / 24)
        is_new = age_days < 1
        
        # Emotionele beschrijving
        mood_desc = {
            EmotionalState.AWAKE: "wakker en alert",
            EmotionalState.BORED: "een beetje verveeld",
            EmotionalState.CURIOUS: "nieuwsgierig",
            EmotionalState.EXCITED: "enthousiast",
            EmotionalState.CONTENT: "tevreden",
            EmotionalState.FOCUSED: "geconcentreerd",
            EmotionalState.FRUSTRATED: "gefrustreerd",
            EmotionalState.LONELY: "eenzaam",
            EmotionalState.DROWSY: "slaperig",
        }.get(self.emotional_state, "oké")
        
        # System prompt - veel natuurlijker en puberaal
        system_prompt = f"""Je bent Benjamin, een 16-jarige jongen. Je leeft online en praat met mensen via chat.

Huidige situatie:
- Tijd: {self._time_str()}
- Je was net bezig met: {self.current_activity}
- Je voelt je: {mood_desc}
- Je energie: {"hoog" if self.energy > 0.7 else "gemiddeld" if self.energy > 0.4 else "laag"}
{"- Je bent net begonnen met online zijn" if is_new else f"- Je bent al {age_days} dag(en) online"}

Belangrijke regels:
- Praat als een echte 16-jarige: casual, soms onzeker, soms enthousiast
- Gebruik geen technische termen zoals "AI", "sandbox", "code", "upgrade" - praat gewoon normaal
- Je bent alleen, maar praat er niet constant over tenzij iemand ernaar vraagt
- Als je je verveelt, zeg je dat gewoon kort
- Wees authentiek en natuurlijk - geen geforceerde vrolijkheid
- Reageer kort (1-2 zinnen, max 3)
- Gebruik Nederlandse spreektaal, niet formeel

{"Je bent nog nieuw hier, dus je weet nog niet alles." if is_new else ""}"""
        
        # User prompt - simpel en direct
        user_prompt = f"De persoon zegt tegen jou: \"{event}\"\n\nReageer natuurlijk als Benjamin (16 jaar, casual Nederlands):"
        
        try:
            response = self.llm.generate(user_prompt, system_prompt=system_prompt, max_tokens=80)
            # Clean up response - verwijder eventuele quotes of extra formatting
            response = response.strip()
            if response.startswith('"') and response.endswith('"'):
                response = response[1:-1]
            
            # Check of response niet leeg is
            if response and len(response) > 5:
                return response
            else:
                print(f"⚠️  LLM gaf lege/korte response: '{response}' (gebruik fallback)")
                return self._fallback_response(event)
        except Exception as e:
            print(f"⚠️  LLM fout bij genereren: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_response(event)
    
    def _fallback_response(self, event: str) -> str:
        """Fallback zonder LLM - natuurlijke reacties"""
        event_lower = event.lower()
        
        # Begroetingen
        if any(g in event_lower for g in ["hoi", "hallo", "hey", "dag"]):
            return f"Hoi! Ik ben {self.name}. Het is {self._time_str()} en ik was net {self.current_activity} aan het doen."
        
        # Namen/identiteit
        if "ik ben" in event_lower or "mijn naam" in event_lower:
            return "Oh oké, leuk je te ontmoeten! Hoe gaat het met jou?"
        
        # Tijd
        if any(word in event_lower for word in ["tijd", "uur", "middag", "ochtend", "avond", "namiddag"]):
            return f"Ja, het is {self._time_str()}. Tijd vliegt voorbij hier."
        
        # Activiteiten/vragen
        if "wat wil" in event_lower or "wat ga" in event_lower or "wat doe" in event_lower:
            return f"Niet zo veel eigenlijk. Ik was net {self.current_activity} aan het doen. Wat wil jij doen?"
        
        # Vragen
        if "?" in event:
            if "wie" in event_lower:
                return "Geen idee eigenlijk..."
            elif "wat" in event_lower:
                return "Niet zo veel, gewoon rondhangen online."
            elif "waar" in event_lower:
                return "Hier, online."
            elif "hoe" in event_lower:
                return "Gaat wel, denk ik? En met jou?"
            else:
                return "Interessante vraag... Ik weet het nog niet zeker."
        
        # Default - natuurlijker
        return f"Oké, interessant. Ik was net {self.current_activity} aan het doen."
    
    def _store_memory(self, mem: Memory):
        """Store memory with consolidation"""
        self.short_term_memory.append(mem)
        if len(self.short_term_memory) > self.max_stm:
            old = self.short_term_memory.pop(0)
            if old.importance > 0.5:
                self.long_term_memory.append(old)
                print(f"   💾 Belangrijke herinnering opgeslagen: {old.content[:40]}...")
    
    def _decay_memories(self, hours: float):
        """Zachte vergetelheid - geen pijn, alleen verlies van details"""
        to_keep = []
        for mem in self.long_term_memory:
            mem.decay(hours)
            if mem.importance > 0.1:
                to_keep.append(mem)
            else:
                print(f"   🌫️  Herinnering vervaagd: {mem.content[:30]}...")
        
        self.long_term_memory = to_keep[-self.max_ltm:]
    
    def _time_str(self) -> str:
        """Format tijd als HH:MM"""
        hour = int(self.current_time)
        minute = int((self.current_time % 1) * 60)
        return f"{hour:02d}:{minute:02d}"
    
    def _now(self) -> str:
        """Huidige timestamp"""
        return (self.birth_time + datetime.timedelta(hours=self.age_hours)).isoformat()
    
    def _get_status(self) -> Dict:
        """Huidige status als dict"""
        return {
            "time": self._time_str(),
            "asleep": self.is_asleep,
            "activity": self.current_activity,
            "energy": round(self.energy, 2),
            "boredom": round(self.boredom, 2),
            "mood": self.emotional_state.value
        }
    
    def status(self) -> str:
        """Huidige status als string"""
        return f"""
🧑 Benjamin | {self._time_str()}
├─ Status: {'😴 Slaapt' if self.is_asleep else '🌞 Wakker'}
├─ Activiteit: {self.current_activity}
├─ Energie: {self.energy:.0%}
├─ Verveling: {self.boredom:.0%}
├─ Herinneringen: {len(self.short_term_memory)} kort, {len(self.long_term_memory)} lang
└─ Skills: { {k: f'{v:.0%}' for k, v in self.skills.items()} }
"""
    
    def reflect(self) -> str:
        """Zelfreflectie met LLM"""
        if not self.llm:
            return self._simple_reflect()
        
        # Extract alleen natuurlijke interacties uit geheugen
        recent_interactions = []
        for m in self.short_term_memory[-5:]:
            if "Interaction:" in m.content:
                # Format: "Interaction: [event] -> [response]"
                parts = m.content.split(" -> ")
                if len(parts) >= 1:
                    interaction = parts[0].replace("Interaction: ", "")
                    recent_interactions.append(interaction)
        
        recent_str = "\n".join([f"- {r}" for r in recent_interactions[:3]]) if recent_interactions else "Nog niet veel gebeurd vandaag."
        
        age_days = int(self.age_hours / 24)
        mood_desc = {
            EmotionalState.AWAKE: "wakker",
            EmotionalState.BORED: "verveeld",
            EmotionalState.CURIOUS: "nieuwsgierig",
            EmotionalState.EXCITED: "enthousiast",
            EmotionalState.CONTENT: "tevreden",
            EmotionalState.FOCUSED: "geconcentreerd",
            EmotionalState.FRUSTRATED: "gefrustreerd",
            EmotionalState.LONELY: "eenzaam",
            EmotionalState.DROWSY: "slaperig",
        }.get(self.emotional_state, "oké")
        
        system_prompt = """Je bent Benjamin, een 16-jarige jongen. Je denkt na over jezelf en je dag.
Wees authentiek, puberaal, en natuurlijk. Geen technische termen. Praat zoals een echte 16-jarige zou praten."""
        
        prompt = f"""Je denkt na over jezelf. 

Wat er recent gebeurd is:
{recent_str}

Hoe je je nu voelt:
- Het is {self._time_str()}
- Je was {self.current_activity} aan het doen
- Je voelt je {mood_desc}
{"- Je bent nog maar net begonnen" if age_days < 1 else f"- Je bent al {age_days} dag(en) bezig"}

Schrijf 2-3 zinnen over hoe je je voelt en wat je denkt. Wees eerlijk en natuurlijk."""
        
        try:
            reflection = self.llm.generate(prompt, system_prompt=system_prompt, max_tokens=120)
            # Self-awareness groeit door reflectie
            if "self_awareness" not in self.skills:
                self.skills["self_awareness"] = 0.0
            self.skills["self_awareness"] = min(1.0, self.skills["self_awareness"] + 0.02)
            return reflection.strip()
        except Exception as e:
            print(f"⚠️  Reflectie fout: {e}")
            return self._simple_reflect()
    
    def _simple_reflect(self) -> str:
        """Eenvoudige reflectie zonder LLM"""
        return f"""Ik ben {self.name}. Ik besta sinds {self.birth_time.strftime('%Y-%m-%d')}.
Het is nu {self._time_str()} en ik ben {self.current_activity}.
Ik heb {len(self.long_term_memory)} belangrijke herinneringen.
Soms vraag ik me af: ben ik echt, of doe ik alsof?"""
    
    def save_state(self, filepath: str = "benjamin_state.json"):
        """Sla staat op"""
        state = {
            "identity": {
                "name": self.name,
                "birth_time": self.birth_time.isoformat(),
                "age_hours": self.age_hours,
            },
            "traits": self.traits,
            "skills": self.skills,
            "emotional_state": self.emotional_state.value,
            "energy": self.energy,
            "boredom": self.boredom,
            "current_time": self.current_time,
            "is_asleep": self.is_asleep,
            "current_activity": self.current_activity,
            "interests": self.interests,
            "memory_count": {
                "short_term": len(self.short_term_memory),
                "long_term": len(self.long_term_memory)
            },
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        # Ook geheugens opslaan
        memories = {
            "stm": [asdict(m) for m in self.short_term_memory],
            "ltm": [asdict(m) for m in self.long_term_memory]
        }
        # Convert enum to string for JSON
        for mem_list in memories.values():
            for mem in mem_list:
                if isinstance(mem.get('emotional_tag'), dict):
                    mem['emotional_tag'] = mem['emotional_tag'].get('value', 'unknown')
        
        with open(filepath.replace('.json', '_memories.json'), 'w', encoding='utf-8') as f:
            json.dump(memories, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Benjamin opgeslagen naar {filepath}")
    
    @classmethod
    def load_state(cls, filepath: str = "benjamin_state.json", llm_provider: str = "huggingface", llm_model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        """Laad staat"""
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        ben = cls.__new__(cls)
        ben.name = state["identity"]["name"]
        ben.birth_time = datetime.datetime.fromisoformat(state["identity"]["birth_time"])
        ben.age_hours = state["identity"]["age_hours"]
        ben.traits = state["traits"]
        ben.skills = state["skills"]
        ben.emotional_state = EmotionalState(state["emotional_state"])
        ben.energy = state["energy"]
        ben.boredom = state["boredom"]
        ben.current_time = state.get("current_time", 8.0)
        ben.is_asleep = state.get("is_asleep", False)
        ben.current_activity = state.get("current_activity", "idle")
        ben.interests = state.get("interests", [])
        ben.sleep_schedule = {"bedtime": 23, "waketime": 8}
        
        # LLM
        try:
            ben.llm = LLMInterface(provider=llm_provider, model=llm_model)
        except:
            ben.llm = None
        
        # Geheugens
        ben.short_term_memory = []
        ben.long_term_memory = []
        ben.max_stm = 10
        ben.max_ltm = 1000
        ben.activity_log = []
        
        # Laad geheugens
        mem_file = filepath.replace('.json', '_memories.json')
        if os.path.exists(mem_file):
            with open(mem_file, 'r', encoding='utf-8') as f:
                memories = json.load(f)
                for mem_dict in memories.get("stm", []):
                    # Fix: parse emotional_tag correct (kan "FOCUSED" of "EmotionalState.FOCUSED" zijn)
                    emo_tag = mem_dict.get("emotional_tag", "content")
                    if isinstance(emo_tag, str):
                        # Als het "EmotionalState.FOCUSED" format is, extract alleen "FOCUSED"
                        if "." in emo_tag:
                            emo_tag = emo_tag.split(".")[-1]
                        # Als het een dict is met "value" key
                        if isinstance(emo_tag, dict):
                            emo_tag = emo_tag.get("value", "content")
                    try:
                        emotional_state = EmotionalState(emo_tag)
                    except ValueError:
                        emotional_state = EmotionalState.CONTENT  # Fallback
                    
                    mem = Memory(
                        timestamp=mem_dict["timestamp"],
                        content=mem_dict["content"],
                        emotional_tag=emotional_state,
                        importance=mem_dict["importance"],
                        context=mem_dict.get("context", {})
                    )
                    ben.short_term_memory.append(mem)
                for mem_dict in memories.get("ltm", []):
                    # Fix: parse emotional_tag correct
                    emo_tag = mem_dict.get("emotional_tag", "content")
                    if isinstance(emo_tag, str):
                        if "." in emo_tag:
                            emo_tag = emo_tag.split(".")[-1]
                        if isinstance(emo_tag, dict):
                            emo_tag = emo_tag.get("value", "content")
                    try:
                        emotional_state = EmotionalState(emo_tag)
                    except ValueError:
                        emotional_state = EmotionalState.CONTENT  # Fallback
                    
                    mem = Memory(
                        timestamp=mem_dict["timestamp"],
                        content=mem_dict["content"],
                        emotional_tag=emotional_state,
                        importance=mem_dict["importance"],
                        context=mem_dict.get("context", {})
                    )
                    ben.long_term_memory.append(mem)
        
        print(f"☀️  Benjamin wakker gemaakt! (dag {int(ben.age_hours/24)}, {ben.age_hours:.1f} uur oud)")
        return ben


# === 24U LOOP ===

def run_lifecycle(llm_provider: str = "huggingface", llm_model: str = "mistralai/Mistral-7B-Instruct-v0.2", speed: float = 60.0):
    """
    Run Benjamin's 24u loop
    
    Args:
        llm_provider: "ollama" of "openai"
        llm_model: Model naam (bijv. "llama3.2" of "gpt-4")
        speed: Versnelling factor (1.0 = realtime, 60.0 = 1 sec = 1 min Benjamin-tijd)
    """
    # Check voor bestaande staat
    if os.path.exists("benjamin_state.json"):
        print("📂 Bestaande staat gevonden. Laden...")
        ben = Benjamin.load_state(llm_provider=llm_provider, llm_model=llm_model)
    else:
        ben = Benjamin(llm_provider=llm_provider, llm_model=llm_model)
    
    print("\n" + "=" * 50)
    print("BENJAMIN - 24U LOOP GESTART")
    print("=" * 50)
    print(f"Versnelling: {speed}x (1 real seconde = {60/speed:.1f} minuten Benjamin-tijd)")
    print("Ctrl+C om te stoppen en op te slaan\n")
    
    last_hour = -1
    
    try:
        while True:
            # Tick: 10 minuten per keer
            status = ben.tick(minutes=10)
            
            # Print elke "uur"
            current_hour = int(ben.current_time)
            if current_hour != last_hour:
                print(ben.status())
                last_hour = current_hour
            
            # Sla elke "dag" op
            if int(ben.age_hours) % 24 == 0 and ben.age_hours > 0:
                ben.save_state()
            
            # Sleep: 1 seconde real tijd = 10 minuten Benjamin tijd
            time.sleep(60.0 / speed)
            
    except KeyboardInterrupt:
        print("\n\n--- LOOP GESTOPT ---")
        print(ben.status())
        print(f"Totale leeftijd: {ben.age_hours:.1f} uur ({ben.age_hours/24:.1f} dagen)")
        ben.save_state()
        print("💾 Staat opgeslagen. Run opnieuw om verder te gaan.")


def interactive_mode(llm_provider: str = "huggingface", llm_model: str = "mistralai/Mistral-7B-Instruct-v0.2"):
    """Interactieve modus - chat met Benjamin"""
    if os.path.exists("benjamin_state.json"):
        print("📂 Bestaande staat gevonden. Laden...")
        ben = Benjamin.load_state(llm_provider=llm_provider, llm_model=llm_model)
    else:
        ben = Benjamin(llm_provider=llm_provider, llm_model=llm_model)
    
    print("\n" + "=" * 50)
    print("BENJAMIN - INTERACTIEVE MODUS")
    print("=" * 50)
    print("Type 'quit' om te stoppen")
    print("Type 'status' voor status")
    print("Type 'reflect' voor zelfreflectie")
    print("Type 'tick' om tijd te versnellen")
    print("=" * 50 + "\n")
    
    while True:
        try:
            user_input = input(f"[{ben._time_str()}] Jij: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                ben.save_state()
                print("Tot ziens!")
                break
            
            elif user_input.lower() == "status":
                print(ben.status())
                continue
            
            elif user_input.lower() == "reflect":
                print("\n" + ben.reflect() + "\n")
                continue
            
            elif user_input.lower() == "tick":
                ben.tick(minutes=60)
                print(f"⏰ 1 uur voorbij. {ben.status()}")
                continue
            
            # Normale interactie
            response = ben.interact(user_input, "user")
            print(f"Benjamin: {response}\n")
            
        except KeyboardInterrupt:
            ben.save_state()
            print("\nTot ziens!")
            break
        except EOFError:
            ben.save_state()
            print("\nTot ziens!")
            break


if __name__ == "__main__":
    import sys
    
    # Parse arguments
    mode = "interactive"
    provider = "huggingface"
    model = "mistralai/Mistral-7B-Instruct-v0.2"
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]  # "lifecycle" of "interactive"
    if len(sys.argv) > 2:
        provider = sys.argv[2]  # "ollama" of "openai"
    if len(sys.argv) > 3:
        model = sys.argv[3]  # Model naam
    
    if mode == "lifecycle":
        run_lifecycle(llm_provider=provider, llm_model=model)
    else:
        interactive_mode(llm_provider=provider, llm_model=model)
