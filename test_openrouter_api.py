#!/usr/bin/env python3
"""
Script per testare l'API Key di OpenRouter e mostrare tutte le funzionalità disponibili
OpenRouter ti permette di accedere a molti modelli AI diversi incluso Gemini!
"""

import os
import json
import requests
import time
from typing import Dict, List, Any

class OpenRouterAPITester:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:3000",  # Opzionale per rankings
            "X-Title": "API Tester"  # Opzionale per rankings
        }
    
    def test_connection(self) -> bool:
        """Test se l'API key è valida"""
        print("🔍 Testing OpenRouter API Key validity...")
        
        try:
            url = f"{self.base_url}/models"
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
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                models = response.json().get('data', [])
                
                # Categorie di modelli interessanti
                categories = {
                    "🧠 Gemini Models": ["gemini", "google"],
                    "🤖 GPT Models": ["gpt", "openai"],
                    "🦙 Llama Models": ["llama", "meta"],
                    "🔥 Claude Models": ["claude", "anthropic"],
                    "⚡ Other Popular": ["mistral", "cohere", "perplexity"]
                }
                
                found_models = {cat: [] for cat in categories}
                
                for model in models:
                    model_id = model.get('id', '').lower()
                    model_name = model.get('name', model.get('id', 'Unknown'))
                    
                    for category, keywords in categories.items():
                        if any(keyword in model_id for keyword in keywords):
                            found_models[category].append({
                                'id': model.get('id'),
                                'name': model_name,
                                'context_length': model.get('context_length', 'Unknown'),
                                'pricing': model.get('pricing', {})
                            })
                            break
                
                # Mostra i modelli per categoria
                for category, models_list in found_models.items():
                    if models_list:
                        print(f"\n{category}:")
                        for model in models_list[:5]:  # Mostra solo i primi 5 per categoria
                            pricing_prompt = model['pricing'].get('prompt', 'Free')
                            pricing_completion = model['pricing'].get('completion', 'Free')
                            print(f"  🤖 {model['name']}")
                            print(f"     ID: {model['id']}")
                            print(f"     Context: {model['context_length']}")
                            print(f"     Cost: {pricing_prompt}/{pricing_completion}")
                            print()
                
                print(f"Total models available: {len(models)}")
                return models
            else:
                print(f"❌ Error fetching models: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def test_gemini_text_generation(self) -> bool:
        """Test generazione di testo con Gemini tramite OpenRouter"""
        print("\n💬 Testing Gemini Text Generation:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {
                        "role": "user",
                        "content": "Ciao! Puoi dirmi 3 curiosità interessanti sull'intelligenza artificiale?"
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['choices'][0]['message']['content']
                print("✅ Gemini Text Generation SUCCESS!")
                print(f"Response: {text_response[:300]}...")
                
                # Mostra info sull'utilizzo
                usage = result.get('usage', {})
                print(f"Tokens used: {usage.get('total_tokens', 'Unknown')}")
                return True
            else:
                print(f"❌ Gemini Text Generation FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_gemini_vision(self) -> bool:
        """Test analisi di immagini con Gemini Vision"""
        print("\n👁️ Testing Gemini Vision:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Descrivi questa immagine in dettaglio"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['choices'][0]['message']['content']
                print("✅ Gemini Vision SUCCESS!")
                print(f"Image description: {text_response[:300]}...")
                return True
            else:
                print(f"❌ Gemini Vision FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_gpt_generation(self) -> bool:
        """Test generazione con GPT tramite OpenRouter"""
        print("\n🤖 Testing GPT Generation:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": "Scrivi una breve poesia sull'intelligenza artificiale"
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.8
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['choices'][0]['message']['content']
                print("✅ GPT Generation SUCCESS!")
                print(f"Poetry: {text_response[:200]}...")
                return True
            else:
                print(f"❌ GPT Generation FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_claude_generation(self) -> bool:
        """Test generazione con Claude tramite OpenRouter"""
        print("\n🔥 Testing Claude Generation:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "anthropic/claude-3-haiku:beta",
                "messages": [
                    {
                        "role": "user",
                        "content": "Spiega in modo semplice cos'è il machine learning"
                    }
                ],
                "max_tokens": 250
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['choices'][0]['message']['content']
                print("✅ Claude Generation SUCCESS!")
                print(f"Explanation: {text_response[:200]}...")
                return True
            else:
                print(f"❌ Claude Generation FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_code_generation(self) -> bool:
        """Test generazione di codice"""
        print("\n💻 Testing Code Generation:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {
                        "role": "user",
                        "content": "Scrivi una funzione Python che calcola la sequenza di Fibonacci"
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.3
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['choices'][0]['message']['content']
                print("✅ Code Generation SUCCESS!")
                print(f"Generated code: {text_response[:300]}...")
                return True
            else:
                print(f"❌ Code Generation FAILED: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_conversation(self) -> bool:
        """Test conversazione multi-turn"""
        print("\n💭 Testing Multi-turn Conversation:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {"role": "user", "content": "Ciao, sono un sviluppatore"},
                    {"role": "assistant", "content": "Ciao! Piacere di conoscerti. Che tipo di sviluppo fai?"},
                    {"role": "user", "content": "Lavoro principalmente con Python. Puoi consigliarmi una libreria per l'AI?"}
                ],
                "max_tokens": 200
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['choices'][0]['message']['content']
                print("✅ Multi-turn Conversation SUCCESS!")
                print(f"Response: {text_response[:200]}...")
                return True
            else:
                print(f"❌ Conversation FAILED: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def get_account_info(self) -> Dict:
        """Ottieni informazioni sull'account"""
        print("\n📊 Account Information:")
        
        try:
            url = f"{self.base_url}/auth/key"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                account_data = response.json()
                print("✅ Account info retrieved!")
                
                # Mostra informazioni utili
                if 'data' in account_data:
                    data = account_data['data']
                    print(f"Label: {data.get('label', 'N/A')}")
                    print(f"Usage: ${data.get('usage', 0):.4f}")
                    print(f"Limit: ${data.get('limit', 'Unlimited')}")
                    print(f"Rate Limit: {data.get('rate_limit', {})}")
                
                return {"status": "success", "data": account_data}
            else:
                print("⚠️ Account info not accessible")
                return {"status": "limited_access"}
                
        except Exception as e:
            print(f"⚠️ Error getting account info: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Esegui tutti i test"""
        print("🚀 Starting OpenRouter API Comprehensive Test")
        print("=" * 60)
        
        results = {}
        
        # Test connessione
        results['connection'] = self.test_connection()
        if not results['connection']:
            print("\n❌ API Key non valida. Impossibile continuare i test.")
            return results
        
        # Lista modelli
        models = self.list_available_models()
        results['models_available'] = len(models) > 0
        
        # Test funzionalità con diversi modelli
        results['gemini_text'] = self.test_gemini_text_generation()
        results['gemini_vision'] = self.test_gemini_vision()
        results['gpt_generation'] = self.test_gpt_generation()
        results['claude_generation'] = self.test_claude_generation()
        results['code_generation'] = self.test_code_generation()
        results['conversation'] = self.test_conversation()
        
        # Informazioni account
        account_info = self.get_account_info()
        results['account_info'] = account_info.get('status') in ['success', 'limited_access']
        
        # Riassunto
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY:")
        print("=" * 60)
        
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
    
    print("🔬 OPENROUTER API TESTER")
    print("=" * 60)
    print("OpenRouter ti permette di accedere a MOLTI modelli AI diversi!")
    print("Inclusi: Gemini, GPT, Claude, Llama e molti altri!")
    print("=" * 60)
    print(f"Testing API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Crea il tester
    tester = OpenRouterAPITester(api_key)
    
    # Esegui tutti i test
    results = tester.run_all_tests()
    
    # Suggerimenti per l'integrazione
    print("\n" + "=" * 60)
    print("💡 INTEGRATION SUGGESTIONS:")
    print("=" * 60)
    
    if results.get('connection', False):
        print("✅ Your OpenRouter API key works! Here's how to integrate it:")
        print()
        print("1. 📦 Install required packages:")
        print("   pip install requests openai")
        print()
        print("2. 🔧 Basic integration example:")
        print("""
   import requests
   import json
   
   def chat_with_ai(message, model="google/gemini-2.0-flash-exp:free"):
       response = requests.post(
           url="https://openrouter.ai/api/v1/chat/completions",
           headers={
               "Authorization": "Bearer YOUR_API_KEY",
               "Content-Type": "application/json"
           },
           json={
               "model": model,
               "messages": [{"role": "user", "content": message}]
           }
       )
       return response.json()['choices'][0]['message']['content']
        """)
        print()
        print("3. 🌟 Available capabilities for your app:")
        
        if results.get('gemini_text', False):
            print("   ✅ Gemini Text Generation - Google's latest AI")
        if results.get('gemini_vision', False):
            print("   ✅ Gemini Vision - Image analysis and description")
        if results.get('gpt_generation', False):
            print("   ✅ GPT Models - OpenAI's powerful language models")
        if results.get('claude_generation', False):
            print("   ✅ Claude Models - Anthropic's AI assistant")
        if results.get('code_generation', False):
            print("   ✅ Code Generation - Programming assistance")
        if results.get('conversation', False):
            print("   ✅ Multi-turn Conversations - Context-aware chat")
        
        print()
        print("4. 🚀 Recommended models for different tasks:")
        print("   • Chat/General: google/gemini-2.0-flash-exp:free")
        print("   • Vision/Images: google/gemini-2.0-flash-exp:free")
        print("   • Code: openai/gpt-4o-mini")
        print("   • Creative: anthropic/claude-3-haiku:beta")
        print("   • Fast/Cheap: meta-llama/llama-3.2-3b-instruct:free")
        
        print()
        print("5. 💰 Cost optimization tips:")
        print("   • Use :free models when possible")
        print("   • Monitor token usage")
        print("   • Choose the right model for the task")
        print("   • Implement caching for repeated queries")
        
    else:
        print("❌ API key is not working. Please check:")
        print("   • API key is correct")
        print("   • Account has sufficient credits")
        print("   • API quotas are not exceeded")
        print("   • Visit https://openrouter.ai/keys to manage your key")


if __name__ == "__main__":
    main()