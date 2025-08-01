#!/usr/bin/env python3
"""
Esempio pratico di integrazione di Gemini AI in una applicazione
"""

import google.generativeai as genai
import os
from typing import List, Dict, Optional
import json

class GeminiChatBot:
    """
    Classe per creare un chatbot con Gemini AI
    """
    
    def __init__(self, api_key: str):
        """Inizializza il chatbot"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.conversation_history: List[Dict] = []
    
    def chat(self, message: str) -> str:
        """
        Invia un messaggio al chatbot e riceve una risposta
        
        Args:
            message (str): Il messaggio dell'utente
            
        Returns:
            str: La risposta del chatbot
        """
        try:
            # Genera la risposta
            response = self.model.generate_content(message)
            
            # Salva nella cronologia
            self.conversation_history.append({
                "user": message,
                "bot": response.text,
                "timestamp": self._get_timestamp()
            })
            
            return response.text
            
        except Exception as e:
            error_msg = f"Errore nella generazione della risposta: {str(e)}"
            print(error_msg)
            return error_msg
    
    def chat_with_context(self, message: str) -> str:
        """
        Chat con contesto della conversazione precedente
        
        Args:
            message (str): Il messaggio dell'utente
            
        Returns:
            str: La risposta del chatbot
        """
        try:
            # Costruisci il contesto dalla cronologia
            context = self._build_context()
            full_message = f"{context}\n\nUtente: {message}"
            
            response = self.model.generate_content(full_message)
            
            # Salva nella cronologia
            self.conversation_history.append({
                "user": message,
                "bot": response.text,
                "timestamp": self._get_timestamp()
            })
            
            return response.text
            
        except Exception as e:
            error_msg = f"Errore nella generazione della risposta: {str(e)}"
            print(error_msg)
            return error_msg
    
    def analyze_image(self, image_path: str, prompt: str = "Descrivi questa immagine") -> str:
        """
        Analizza un'immagine con Gemini Pro Vision
        
        Args:
            image_path (str): Percorso dell'immagine
            prompt (str): Prompt per l'analisi
            
        Returns:
            str: Descrizione dell'immagine
        """
        try:
            # Usa il modello vision
            vision_model = genai.GenerativeModel('gemini-pro-vision')
            
            # Carica l'immagine
            import PIL.Image
            image = PIL.Image.open(image_path)
            
            # Genera la risposta
            response = vision_model.generate_content([prompt, image])
            
            return response.text
            
        except Exception as e:
            error_msg = f"Errore nell'analisi dell'immagine: {str(e)}"
            print(error_msg)
            return error_msg
    
    def generate_code(self, description: str, language: str = "Python") -> str:
        """
        Genera codice basato su una descrizione
        
        Args:
            description (str): Descrizione di cosa deve fare il codice
            language (str): Linguaggio di programmazione
            
        Returns:
            str: Il codice generato
        """
        prompt = f"Scrivi del codice {language} che: {description}. Fornisci solo il codice con commenti esplicativi."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_msg = f"Errore nella generazione del codice: {str(e)}"
            print(error_msg)
            return error_msg
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """
        Riassume un testo
        
        Args:
            text (str): Testo da riassumere
            max_sentences (int): Numero massimo di frasi nel riassunto
            
        Returns:
            str: Riassunto del testo
        """
        prompt = f"Riassumi il seguente testo in massimo {max_sentences} frasi:\n\n{text}"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_msg = f"Errore nel riassunto: {str(e)}"
            print(error_msg)
            return error_msg
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Traduce un testo
        
        Args:
            text (str): Testo da tradurre
            target_language (str): Lingua di destinazione
            
        Returns:
            str: Testo tradotto
        """
        prompt = f"Traduci il seguente testo in {target_language}:\n\n{text}"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_msg = f"Errore nella traduzione: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_conversation_history(self) -> List[Dict]:
        """Restituisce la cronologia della conversazione"""
        return self.conversation_history
    
    def clear_history(self):
        """Cancella la cronologia della conversazione"""
        self.conversation_history = []
    
    def save_conversation(self, filename: str):
        """Salva la conversazione in un file JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            print(f"Conversazione salvata in {filename}")
        except Exception as e:
            print(f"Errore nel salvare la conversazione: {str(e)}")
    
    def _build_context(self) -> str:
        """Costruisce il contesto dalla cronologia"""
        if not self.conversation_history:
            return ""
        
        context_lines = []
        # Prendi solo gli ultimi 5 scambi per non superare i limiti
        recent_history = self.conversation_history[-5:]
        
        for exchange in recent_history:
            context_lines.append(f"Utente: {exchange['user']}")
            context_lines.append(f"Assistant: {exchange['bot']}")
        
        return "\n".join(context_lines)
    
    def _get_timestamp(self) -> str:
        """Restituisce il timestamp corrente"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def demo_chatbot():
    """Dimostrazione del chatbot"""
    print("🤖 GEMINI CHATBOT DEMO")
    print("=" * 50)
    
    # Inizializza il chatbot con la tua API key
    api_key = "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"
    chatbot = GeminiChatBot(api_key)
    
    print("Chatbot inizializzato! Scrivi 'quit' per uscire.")
    print("Comandi speciali:")
    print("  /code <descrizione> - Genera codice")
    print("  /translate <lingua> <testo> - Traduci testo")
    print("  /summarize <testo> - Riassumi testo")
    print("  /history - Mostra cronologia")
    print("  /clear - Cancella cronologia")
    print("  /save <filename> - Salva conversazione")
    print()
    
    while True:
        try:
            user_input = input("Tu: ").strip()
            
            if user_input.lower() == 'quit':
                break
            
            if user_input.startswith('/code '):
                description = user_input[6:]
                response = chatbot.generate_code(description)
                print(f"🤖 Codice generato:\n{response}\n")
                
            elif user_input.startswith('/translate '):
                parts = user_input[11:].split(' ', 1)
                if len(parts) == 2:
                    language, text = parts
                    response = chatbot.translate_text(text, language)
                    print(f"🤖 Traduzione:\n{response}\n")
                else:
                    print("Uso: /translate <lingua> <testo>")
                    
            elif user_input.startswith('/summarize '):
                text = user_input[11:]
                response = chatbot.summarize_text(text)
                print(f"🤖 Riassunto:\n{response}\n")
                
            elif user_input == '/history':
                history = chatbot.get_conversation_history()
                print(f"📚 Cronologia ({len(history)} scambi):")
                for i, exchange in enumerate(history[-5:], 1):  # Mostra solo gli ultimi 5
                    print(f"  {i}. [{exchange['timestamp']}]")
                    print(f"     Tu: {exchange['user'][:50]}...")
                    print(f"     Bot: {exchange['bot'][:50]}...")
                print()
                
            elif user_input == '/clear':
                chatbot.clear_history()
                print("🗑️ Cronologia cancellata.\n")
                
            elif user_input.startswith('/save '):
                filename = user_input[6:] or "conversation.json"
                chatbot.save_conversation(filename)
                print()
                
            else:
                # Chat normale con contesto
                response = chatbot.chat_with_context(user_input)
                print(f"🤖: {response}\n")
                
        except KeyboardInterrupt:
            print("\n\nArrivederci!")
            break
        except Exception as e:
            print(f"Errore: {str(e)}\n")


if __name__ == "__main__":
    demo_chatbot()