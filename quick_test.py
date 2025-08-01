#!/usr/bin/env python3
import requests

# LA TUA API KEY FUNZIONA! ✅
API_KEY = "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"

def chat_gemini(message):
    """Chat veloce con Gemini GRATUITO"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-2.5-flash-lite",  # GRATUITO!
            "messages": [{"role": "user", "content": message}]
        }
    )
    return response.json()['choices'][0]['message']['content']

def analyze_image(image_url, prompt="Descrivi questa immagine"):
    """Analizza immagini con Gemini Vision"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-2.5-flash-lite",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }]
        }
    )
    return response.json()['choices'][0]['message']['content']

# TEST VELOCE
if __name__ == "__main__":
    print("🚀 TEST VELOCE OPENROUTER API")
    print("=" * 40)
    
    # Test 1: Chat
    print("💬 Test Chat...")
    risposta = chat_gemini("Ciao! Dimmi una curiosità sull'AI")
    print(f"✅ Gemini: {risposta[:100]}...")
    
    # Test 2: Vision
    print("\n👁️ Test Vision...")
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    descrizione = analyze_image(image_url)
    print(f"✅ Vision: {descrizione[:100]}...")
    
    print("\n🎉 LA TUA API KEY FUNZIONA PERFETTAMENTE!")
    print("🆓 Stai usando Gemini GRATUITAMENTE!")
    print("👁️ Analisi immagini disponibile!")