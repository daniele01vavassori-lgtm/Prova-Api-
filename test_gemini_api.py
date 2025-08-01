#!/usr/bin/env python3
"""
Script per testare l'API Key di Gemini AI e mostrare tutte le funzionalità disponibili
"""

import os
import json
import requests
import time
from typing import Dict, List, Any

class GeminiAPITester:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> bool:
        """Test se l'API key è valida"""
        print("🔍 Testing API Key validity...")
        
        try:
            url = f"{self.base_url}/models?key={self.api_key}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ API Key is VALID!")
                return True
            else:
                print(f"❌ API Key is INVALID. Status code: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
            return False
    
    def list_available_models(self) -> List[Dict]:
        """Lista tutti i modelli disponibili"""
        print("\n📋 Available Models:")
        
        try:
            url = f"{self.base_url}/models?key={self.api_key}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                
                for model in models:
                    name = model.get('name', 'Unknown')
                    display_name = model.get('displayName', 'Unknown')
                    description = model.get('description', 'No description')
                    
                    print(f"  🤖 {display_name}")
                    print(f"     Name: {name}")
                    print(f"     Description: {description[:100]}...")
                    print()
                
                return models
            else:
                print(f"❌ Error fetching models: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def test_text_generation(self) -> bool:
        """Test generazione di testo semplice"""
        print("\n💬 Testing Text Generation:")
        
        try:
            url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Ciao! Puoi dirmi 3 curiosità interessanti sull'intelligenza artificiale?"
                    }]
                }]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ Text Generation SUCCESS!")
                print(f"Response: {text_response[:200]}...")
                return True
            else:
                print(f"❌ Text Generation FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_vision_capabilities(self) -> bool:
        """Test capacità di visione (se disponibile)"""
        print("\n👁️ Testing Vision Capabilities:")
        
        try:
            # Test con Gemini Pro Vision
            url = f"{self.base_url}/models/gemini-pro-vision:generateContent?key={self.api_key}"
            
            # Creiamo un'immagine di test semplice (base64 di un piccolo PNG)
            # Questo è un pixel rosso 1x1 in base64
            test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "Descrivi questa immagine"},
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": test_image_base64
                            }
                        }
                    ]
                }]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ Vision Capabilities AVAILABLE!")
                print(f"Response: {text_response[:200]}...")
                return True
            else:
                print(f"⚠️ Vision model might not be available: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ Vision test error: {str(e)}")
            return False
    
    def test_conversation(self) -> bool:
        """Test conversazione multi-turn"""
        print("\n💭 Testing Multi-turn Conversation:")
        
        try:
            url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
            
            # Simuliamo una conversazione
            conversation = [
                {"role": "user", "parts": [{"text": "Ciao, come ti chiami?"}]},
                {"role": "model", "parts": [{"text": "Ciao! Sono Gemini, un'intelligenza artificiale di Google."}]},
                {"role": "user", "parts": [{"text": "Puoi aiutarmi con la programmazione Python?"}]}
            ]
            
            payload = {
                "contents": conversation
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ Multi-turn Conversation SUCCESS!")
                print(f"Response: {text_response[:200]}...")
                return True
            else:
                print(f"❌ Conversation FAILED: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_code_generation(self) -> bool:
        """Test generazione di codice"""
        print("\n💻 Testing Code Generation:")
        
        try:
            url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Scrivi una funzione Python che calcola il fattoriale di un numero"
                    }]
                }]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ Code Generation SUCCESS!")
                print(f"Generated code preview: {text_response[:300]}...")
                return True
            else:
                print(f"❌ Code Generation FAILED: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_safety_settings(self) -> bool:
        """Test impostazioni di sicurezza"""
        print("\n🛡️ Testing Safety Settings:")
        
        try:
            url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Parlami delle best practices per la sicurezza informatica"
                    }]
                }],
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ Safety Settings work correctly!")
                print(f"Response: {text_response[:200]}...")
                return True
            else:
                print(f"❌ Safety Settings test FAILED: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def get_usage_info(self) -> Dict:
        """Ottieni informazioni sull'utilizzo dell'API"""
        print("\n📊 API Usage Information:")
        
        # Nota: Gemini API potrebbe non avere un endpoint specifico per l'utilizzo
        # Ma possiamo mostrare le informazioni sui rate limits dai headers
        try:
            url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Test per ottenere headers"
                    }]
                }]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            print("📈 Response Headers (Rate Limits info):")
            for header, value in response.headers.items():
                if 'rate' in header.lower() or 'limit' in header.lower() or 'quota' in header.lower():
                    print(f"  {header}: {value}")
            
            return {"status": "checked", "headers": dict(response.headers)}
            
        except Exception as e:
            print(f"❌ Error getting usage info: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Esegui tutti i test"""
        print("🚀 Starting Gemini API Comprehensive Test")
        print("=" * 50)
        
        results = {}
        
        # Test connessione
        results['connection'] = self.test_connection()
        if not results['connection']:
            print("\n❌ API Key non valida. Impossibile continuare i test.")
            return results
        
        # Lista modelli
        models = self.list_available_models()
        results['models_available'] = len(models) > 0
        
        # Test funzionalità
        results['text_generation'] = self.test_text_generation()
        results['vision_capabilities'] = self.test_vision_capabilities()
        results['conversation'] = self.test_conversation()
        results['code_generation'] = self.test_code_generation()
        results['safety_settings'] = self.test_safety_settings()
        
        # Informazioni utilizzo
        usage_info = self.get_usage_info()
        results['usage_info'] = usage_info.get('status') == 'checked'
        
        # Riassunto
        print("\n" + "=" * 50)
        print("📋 TEST SUMMARY:")
        print("=" * 50)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        successful_tests = sum(results.values())
        total_tests = len(results)
        
        print(f"\n🎯 Overall Success Rate: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
        
        return results


def main():
    """Funzione principale"""
    # La tua API Key
    api_key = "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"
    
    print("🔬 GEMINI AI API TESTER")
    print("=" * 50)
    print(f"Testing API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Crea il tester
    tester = GeminiAPITester(api_key)
    
    # Esegui tutti i test
    results = tester.run_all_tests()
    
    # Suggerimenti per l'integrazione
    print("\n" + "=" * 50)
    print("💡 INTEGRATION SUGGESTIONS:")
    print("=" * 50)
    
    if results.get('connection', False):
        print("✅ Your API key works! Here's how to integrate it in your app:")
        print()
        print("1. 📦 Install required packages:")
        print("   pip install google-generativeai requests")
        print()
        print("2. 🔧 Basic integration example:")
        print("""
   import google.generativeai as genai
   
   # Configure the API
   genai.configure(api_key='your-api-key-here')
   
   # Create model instance
   model = genai.GenerativeModel('gemini-pro')
   
   # Generate content
   response = model.generate_content('Your prompt here')
   print(response.text)
        """)
        print()
        print("3. 🌟 Available capabilities for your app:")
        
        if results.get('text_generation', False):
            print("   ✅ Text Generation - Chatbots, content creation")
        if results.get('vision_capabilities', False):
            print("   ✅ Vision Analysis - Image description, OCR")
        if results.get('conversation', False):
            print("   ✅ Multi-turn Conversations - Interactive chat")
        if results.get('code_generation', False):
            print("   ✅ Code Generation - Programming assistance")
        if results.get('safety_settings', False):
            print("   ✅ Safety Controls - Content filtering")
        
        print()
        print("4. 🚀 Recommended use cases:")
        print("   • Customer support chatbot")
        print("   • Content generation tool")
        print("   • Code assistant")
        print("   • Document analysis")
        print("   • Educational tutor")
        
    else:
        print("❌ API key is not working. Please check:")
        print("   • API key is correct")
        print("   • API key has proper permissions")
        print("   • Billing is set up (if required)")
        print("   • API quotas are not exceeded")


if __name__ == "__main__":
    main()