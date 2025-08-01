#!/usr/bin/env python3
"""
Applicazione Chatbot completa usando OpenRouter API
Supporta Gemini, GPT, Claude e molti altri modelli AI!
"""

import requests
import json
import os
import time
from datetime import datetime
from typing import List, Dict, Optional
import base64

class OpenRouterChatBot:
    """
    Chatbot avanzato che usa OpenRouter per accedere a diversi modelli AI
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:3000",
            "X-Title": "AI Chatbot App"
        }
        self.conversation_history: List[Dict] = []
        self.current_model = "google/gemini-2.5-flash-lite"  # Modello predefinito
        
        # Modelli disponibili con le loro caratteristiche
        self.available_models = {
            "gemini": {
                "id": "google/gemini-2.5-flash-lite",
                "name": "Gemini 2.5 Flash Lite",
                "description": "Veloce e gratuito, ottimo per chat generale",
                "supports_vision": True,
                "cost": "Gratuito"
            },
            "gemini-pro": {
                "id": "google/gemini-2.5-pro",
                "name": "Gemini 2.5 Pro",
                "description": "Il più potente di Google, per compiti complessi",
                "supports_vision": True,
                "cost": "A pagamento"
            },
            "gpt": {
                "id": "openai/gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "description": "Veloce ed economico, buono per la maggior parte dei compiti",
                "supports_vision": False,
                "cost": "A pagamento"
            },
            "gpt4": {
                "id": "openai/gpt-4o-mini",
                "name": "GPT-4o Mini",
                "description": "Più intelligente ma più costoso",
                "supports_vision": True,
                "cost": "A pagamento"
            },
            "claude": {
                "id": "anthropic/claude-3.7-sonnet",
                "name": "Claude 3.7 Sonnet",
                "description": "Eccellente per scrittura e analisi",
                "supports_vision": True,
                "cost": "A pagamento"
            },
            "llama": {
                "id": "meta-llama/llama-3.2-3b-instruct:free",
                "name": "Llama 3.2 3B",
                "description": "Modello open source gratuito",
                "supports_vision": False,
                "cost": "Gratuito"
            }
        }
    
    def set_model(self, model_key: str) -> bool:
        """Cambia il modello AI da usare"""
        if model_key in self.available_models:
            self.current_model = self.available_models[model_key]["id"]
            print(f"✅ Modello cambiato a: {self.available_models[model_key]['name']}")
            return True
        else:
            print(f"❌ Modello '{model_key}' non trovato.")
            return False
    
    def list_models(self):
        """Mostra tutti i modelli disponibili"""
        print("\n🤖 Modelli AI Disponibili:")
        print("=" * 50)
        
        for key, model in self.available_models.items():
            vision_icon = "👁️" if model["supports_vision"] else "💬"
            cost_icon = "🆓" if model["cost"] == "Gratuito" else "💰"
            current = "⭐ (ATTUALE)" if model["id"] == self.current_model else ""
            
            print(f"{vision_icon} {cost_icon} {key}: {model['name']} {current}")
            print(f"   {model['description']}")
            print(f"   Costo: {model['cost']}")
            print()
    
    def chat(self, message: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Invia un messaggio al chatbot
        """
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": self.current_model,
                "messages": [{"role": "user", "content": message}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Salva nella cronologia
                self.conversation_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "model": self.current_model,
                    "user": message,
                    "ai": ai_response,
                    "tokens": result.get('usage', {}).get('total_tokens', 0)
                })
                
                return ai_response
                
            elif response.status_code == 429:
                return "⚠️ Rate limit raggiunto. Aspetta qualche secondo e riprova."
            else:
                return f"❌ Errore: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Errore di connessione: {str(e)}"
    
    def chat_with_context(self, message: str, context_length: int = 5) -> str:
        """
        Chat con contesto delle conversazioni precedenti
        """
        try:
            url = f"{self.base_url}/chat/completions"
            
            # Costruisci i messaggi con contesto
            messages = []
            
            # Aggiungi le ultime conversazioni come contesto
            recent_history = self.conversation_history[-context_length:]
            for exchange in recent_history:
                messages.append({"role": "user", "content": exchange["user"]})
                messages.append({"role": "assistant", "content": exchange["ai"]})
            
            # Aggiungi il messaggio corrente
            messages.append({"role": "user", "content": message})
            
            payload = {
                "model": self.current_model,
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Salva nella cronologia
                self.conversation_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "model": self.current_model,
                    "user": message,
                    "ai": ai_response,
                    "tokens": result.get('usage', {}).get('total_tokens', 0)
                })
                
                return ai_response
                
            elif response.status_code == 429:
                return "⚠️ Rate limit raggiunto. Aspetta qualche secondo e riprova."
            else:
                return f"❌ Errore: {response.status_code}"
                
        except Exception as e:
            return f"❌ Errore: {str(e)}"
    
    def analyze_image(self, image_url: str, prompt: str = "Descrivi questa immagine") -> str:
        """
        Analizza un'immagine usando modelli con capacità vision
        """
        # Verifica se il modello corrente supporta la visione
        current_model_info = None
        for model_info in self.available_models.values():
            if model_info["id"] == self.current_model:
                current_model_info = model_info
                break
        
        if not current_model_info or not current_model_info["supports_vision"]:
            return "❌ Il modello corrente non supporta l'analisi di immagini. Usa un modello con supporto vision (es. Gemini o GPT-4)."
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": self.current_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ Errore nell'analisi dell'immagine: {response.status_code}"
                
        except Exception as e:
            return f"❌ Errore: {str(e)}"
    
    def generate_code(self, description: str, language: str = "Python") -> str:
        """Genera codice basato su una descrizione"""
        prompt = f"Scrivi del codice {language} che: {description}. Fornisci solo il codice con commenti esplicativi."
        return self.chat(prompt, temperature=0.3)
    
    def translate_text(self, text: str, target_language: str) -> str:
        """Traduce un testo"""
        prompt = f"Traduci il seguente testo in {target_language}:\n\n{text}"
        return self.chat(prompt, temperature=0.5)
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Riassume un testo"""
        prompt = f"Riassumi il seguente testo in massimo {max_sentences} frasi:\n\n{text}"
        return self.chat(prompt, temperature=0.5)
    
    def get_conversation_stats(self) -> Dict:
        """Ottieni statistiche sulla conversazione"""
        if not self.conversation_history:
            return {"total_exchanges": 0, "total_tokens": 0}
        
        total_tokens = sum(exchange.get("tokens", 0) for exchange in self.conversation_history)
        models_used = list(set(exchange["model"] for exchange in self.conversation_history))
        
        return {
            "total_exchanges": len(self.conversation_history),
            "total_tokens": total_tokens,
            "models_used": models_used,
            "session_start": self.conversation_history[0]["timestamp"] if self.conversation_history else None
        }
    
    def save_conversation(self, filename: str = None):
        """Salva la conversazione in un file JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "conversation_history": self.conversation_history,
                    "stats": self.get_conversation_stats()
                }, f, ensure_ascii=False, indent=2)
            print(f"✅ Conversazione salvata in {filename}")
        except Exception as e:
            print(f"❌ Errore nel salvare: {str(e)}")
    
    def clear_history(self):
        """Cancella la cronologia della conversazione"""
        self.conversation_history = []
        print("🗑️ Cronologia cancellata.")


def main():
    """Applicazione principale del chatbot"""
    print("🤖 OPENROUTER AI CHATBOT")
    print("=" * 60)
    print("Accesso a Gemini, GPT, Claude e molti altri modelli AI!")
    print("=" * 60)
    
    # Inizializza il chatbot
    api_key = "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"
    chatbot = OpenRouterChatBot(api_key)
    
    print(f"✅ Chatbot inizializzato con {chatbot.available_models[list(chatbot.available_models.keys())[0]]['name']}")
    print("\n📝 Comandi disponibili:")
    print("  /models - Mostra modelli disponibili")
    print("  /model <nome> - Cambia modello (es. /model gemini)")
    print("  /image <url> - Analizza un'immagine")
    print("  /code <descrizione> - Genera codice")
    print("  /translate <lingua> <testo> - Traduci testo")
    print("  /summarize <testo> - Riassumi testo")
    print("  /stats - Mostra statistiche")
    print("  /save - Salva conversazione")
    print("  /clear - Cancella cronologia")
    print("  /context on/off - Attiva/disattiva contesto")
    print("  /quit - Esci")
    print()
    
    use_context = True
    print("💡 Modalità contesto ATTIVA (il bot ricorda le conversazioni precedenti)")
    print("Scrivi il tuo messaggio o usa un comando...")
    print()
    
    while True:
        try:
            user_input = input("Tu: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == '/quit':
                print("👋 Arrivederci!")
                break
            
            elif user_input == '/models':
                chatbot.list_models()
                
            elif user_input.startswith('/model '):
                model_key = user_input[7:].strip()
                chatbot.set_model(model_key)
                
            elif user_input.startswith('/image '):
                image_url = user_input[7:].strip()
                if image_url:
                    print("🔍 Analizzando l'immagine...")
                    response = chatbot.analyze_image(image_url)
                    print(f"🤖: {response}\n")
                else:
                    print("❌ Fornisci un URL dell'immagine")
                    
            elif user_input.startswith('/code '):
                description = user_input[6:].strip()
                if description:
                    print("💻 Generando codice...")
                    response = chatbot.generate_code(description)
                    print(f"🤖: {response}\n")
                else:
                    print("❌ Fornisci una descrizione del codice")
                    
            elif user_input.startswith('/translate '):
                parts = user_input[11:].split(' ', 1)
                if len(parts) == 2:
                    language, text = parts
                    print("🌍 Traducendo...")
                    response = chatbot.translate_text(text, language)
                    print(f"🤖: {response}\n")
                else:
                    print("❌ Uso: /translate <lingua> <testo>")
                    
            elif user_input.startswith('/summarize '):
                text = user_input[11:].strip()
                if text:
                    print("📄 Riassumendo...")
                    response = chatbot.summarize_text(text)
                    print(f"🤖: {response}\n")
                else:
                    print("❌ Fornisci un testo da riassumere")
                    
            elif user_input == '/stats':
                stats = chatbot.get_conversation_stats()
                print("\n📊 Statistiche Conversazione:")
                print(f"   Scambi totali: {stats['total_exchanges']}")
                print(f"   Token totali: {stats['total_tokens']}")
                print(f"   Modelli usati: {', '.join(stats['models_used'])}")
                if stats['session_start']:
                    print(f"   Inizio sessione: {stats['session_start']}")
                print()
                
            elif user_input == '/save':
                chatbot.save_conversation()
                
            elif user_input == '/clear':
                chatbot.clear_history()
                
            elif user_input == '/context on':
                use_context = True
                print("✅ Modalità contesto ATTIVATA")
                
            elif user_input == '/context off':
                use_context = False
                print("✅ Modalità contesto DISATTIVATA")
                
            else:
                # Chat normale
                print("🤖 Pensando...")
                if use_context:
                    response = chatbot.chat_with_context(user_input)
                else:
                    response = chatbot.chat(user_input)
                print(f"🤖: {response}\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Arrivederci!")
            break
        except Exception as e:
            print(f"❌ Errore imprevisto: {str(e)}")


if __name__ == "__main__":
    main()