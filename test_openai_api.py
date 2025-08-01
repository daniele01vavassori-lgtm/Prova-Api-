#!/usr/bin/env python3
"""
Script per testare l'API Key di OpenAI e mostrare tutte le funzionalità disponibili
"""

import os
import json
import requests
import time
from typing import Dict, List, Any

class OpenAIAPITester:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> bool:
        """Test se l'API key è valida"""
        print("🔍 Testing OpenAI API Key validity...")
        
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
                
                # Filtra e mostra solo i modelli più importanti
                important_models = [
                    'gpt-4', 'gpt-4-turbo', 'gpt-4o', 'gpt-4o-mini',
                    'gpt-3.5-turbo', 'dall-e-3', 'dall-e-2', 
                    'whisper-1', 'tts-1', 'text-embedding-ada-002'
                ]
                
                available_models = []
                for model in models:
                    model_id = model.get('id', '')
                    if any(important in model_id for important in important_models):
                        print(f"  🤖 {model_id}")
                        print(f"     Owner: {model.get('owned_by', 'Unknown')}")
                        available_models.append(model)
                
                print(f"\nTotal models available: {len(models)}")
                print(f"Important models shown: {len(available_models)}")
                return models
            else:
                print(f"❌ Error fetching models: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def test_text_generation(self) -> bool:
        """Test generazione di testo con GPT"""
        print("\n💬 Testing Text Generation (GPT):")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "gpt-3.5-turbo",
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
                print("✅ Text Generation SUCCESS!")
                print(f"Response: {text_response[:200]}...")
                
                # Mostra info sull'utilizzo
                usage = result.get('usage', {})
                print(f"Tokens used: {usage.get('total_tokens', 'Unknown')}")
                return True
            else:
                print(f"❌ Text Generation FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_image_generation(self) -> bool:
        """Test generazione di immagini con DALL-E"""
        print("\n🎨 Testing Image Generation (DALL-E):")
        
        try:
            url = f"{self.base_url}/images/generations"
            
            payload = {
                "model": "dall-e-2",
                "prompt": "A cute robot learning to code, digital art style",
                "n": 1,
                "size": "256x256"
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                print("✅ Image Generation SUCCESS!")
                print(f"Generated image URL: {image_url}")
                return True
            else:
                print(f"❌ Image Generation FAILED: {response.status_code}")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_embeddings(self) -> bool:
        """Test generazione di embeddings"""
        print("\n🔢 Testing Text Embeddings:")
        
        try:
            url = f"{self.base_url}/embeddings"
            
            payload = {
                "model": "text-embedding-ada-002",
                "input": "This is a test sentence for embedding generation."
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                embedding = result['data'][0]['embedding']
                print("✅ Embeddings Generation SUCCESS!")
                print(f"Embedding dimensions: {len(embedding)}")
                print(f"First 5 values: {embedding[:5]}")
                
                usage = result.get('usage', {})
                print(f"Tokens used: {usage.get('total_tokens', 'Unknown')}")
                return True
            else:
                print(f"❌ Embeddings FAILED: {response.status_code}")
                print(f"Error: {response.text}")
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
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Ciao, come ti chiami?"},
                    {"role": "assistant", "content": "Ciao! Sono ChatGPT, un'intelligenza artificiale creata da OpenAI."},
                    {"role": "user", "content": "Puoi aiutarmi con la programmazione Python?"}
                ],
                "max_tokens": 200,
                "temperature": 0.7
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
    
    def test_code_generation(self) -> bool:
        """Test generazione di codice"""
        print("\n💻 Testing Code Generation:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": "Scrivi una funzione Python che calcola il fattoriale di un numero"
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
                print(f"Generated code preview: {text_response[:300]}...")
                return True
            else:
                print(f"❌ Code Generation FAILED: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def test_function_calling(self) -> bool:
        """Test chiamata di funzioni"""
        print("\n🔧 Testing Function Calling:")
        
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": "Che tempo fa a Roma oggi?"
                    }
                ],
                "functions": [
                    {
                        "name": "get_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA"
                                }
                            },
                            "required": ["location"]
                        }
                    }
                ],
                "function_call": "auto"
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']
                
                if 'function_call' in message:
                    function_call = message['function_call']
                    print("✅ Function Calling SUCCESS!")
                    print(f"Function called: {function_call['name']}")
                    print(f"Arguments: {function_call['arguments']}")
                else:
                    print("✅ Function Calling available but not triggered in this example")
                    print(f"Response: {message['content'][:100]}...")
                
                return True
            else:
                print(f"❌ Function Calling FAILED: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def get_usage_info(self) -> Dict:
        """Ottieni informazioni sull'utilizzo dell'API"""
        print("\n📊 API Usage Information:")
        
        try:
            # OpenAI doesn't have a direct usage endpoint, but we can check billing
            url = f"{self.base_url}/usage"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                usage_data = response.json()
                print("✅ Usage data retrieved!")
                return {"status": "success", "data": usage_data}
            else:
                print("⚠️ Usage endpoint not accessible (might require different permissions)")
                return {"status": "limited_access"}
                
        except Exception as e:
            print(f"⚠️ Error getting usage info: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Esegui tutti i test"""
        print("🚀 Starting OpenAI API Comprehensive Test")
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
        results['image_generation'] = self.test_image_generation()
        results['embeddings'] = self.test_embeddings()
        results['conversation'] = self.test_conversation()
        results['code_generation'] = self.test_code_generation()
        results['function_calling'] = self.test_function_calling()
        
        # Informazioni utilizzo
        usage_info = self.get_usage_info()
        results['usage_info'] = usage_info.get('status') in ['success', 'limited_access']
        
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
    
    print("🔬 OPENAI API TESTER")
    print("=" * 50)
    print(f"Testing API Key: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Crea il tester
    tester = OpenAIAPITester(api_key)
    
    # Esegui tutti i test
    results = tester.run_all_tests()
    
    # Suggerimenti per l'integrazione
    print("\n" + "=" * 50)
    print("💡 INTEGRATION SUGGESTIONS:")
    print("=" * 50)
    
    if results.get('connection', False):
        print("✅ Your OpenAI API key works! Here's how to integrate it in your app:")
        print()
        print("1. 📦 Install required packages:")
        print("   pip install openai requests")
        print()
        print("2. 🔧 Basic integration example:")
        print("""
   import openai
   
   # Configure the API
   openai.api_key = 'your-api-key-here'
   
   # Generate text
   response = openai.ChatCompletion.create(
       model="gpt-3.5-turbo",
       messages=[{"role": "user", "content": "Hello!"}]
   )
   print(response.choices[0].message.content)
        """)
        print()
        print("3. 🌟 Available capabilities for your app:")
        
        if results.get('text_generation', False):
            print("   ✅ Text Generation - Chatbots, content creation")
        if results.get('image_generation', False):
            print("   ✅ Image Generation - DALL-E artwork creation")
        if results.get('embeddings', False):
            print("   ✅ Text Embeddings - Semantic search, similarity")
        if results.get('conversation', False):
            print("   ✅ Multi-turn Conversations - Interactive chat")
        if results.get('code_generation', False):
            print("   ✅ Code Generation - Programming assistance")
        if results.get('function_calling', False):
            print("   ✅ Function Calling - Tool integration")
        
        print()
        print("4. 🚀 Recommended use cases:")
        print("   • AI-powered chatbot")
        print("   • Content generation tool")
        print("   • Code assistant/copilot")
        print("   • Image generation app")
        print("   • Document analysis with embeddings")
        print("   • Smart search functionality")
        
    else:
        print("❌ API key is not working. Please check:")
        print("   • API key is correct")
        print("   • API key has proper permissions")
        print("   • Billing is set up")
        print("   • API quotas are not exceeded")
        print("   • Account is in good standing")


if __name__ == "__main__":
    main()