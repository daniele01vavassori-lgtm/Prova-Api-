#!/usr/bin/env python3
"""
App Web per testare OpenRouter API
Interfaccia semplice per chattare con Gemini e altri modelli AI
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import json
import os

app = Flask(__name__)

# La tua API Key
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"

# Modelli disponibili
MODELS = {
    "gemini": {
        "id": "google/gemini-2.5-flash-lite",
        "name": "Gemini 2.5 Flash Lite",
        "description": "GRATUITO - Veloce e potente",
        "free": True
    },
    "gemini-pro": {
        "id": "google/gemini-2.5-pro", 
        "name": "Gemini 2.5 Pro",
        "description": "A pagamento - Il più potente",
        "free": False
    },
    "gpt": {
        "id": "openai/gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo", 
        "description": "A pagamento - Veloce",
        "free": False
    },
    "llama": {
        "id": "meta-llama/llama-3.2-3b-instruct:free",
        "name": "Llama 3.2 3B",
        "description": "GRATUITO - Open source",
        "free": True
    }
}

def chat_with_ai(message, model_id, max_tokens=500):
    """Invia messaggio all'AI"""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": result['choices'][0]['message']['content'],
                "tokens": result.get('usage', {}).get('total_tokens', 0)
            }
        elif response.status_code == 429:
            return {
                "success": False,
                "error": "Rate limit raggiunto. Aspetta qualche secondo."
            }
        else:
            return {
                "success": False,
                "error": f"Errore API: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Errore: {str(e)}"
        }

def analyze_image_ai(image_url, prompt, model_id):
    """Analizza immagine con AI"""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_id,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }],
            "max_tokens": 500
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": result['choices'][0]['message']['content']
            }
        else:
            return {
                "success": False,
                "error": f"Errore: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Errore: {str(e)}"
        }

@app.route('/')
def index():
    """Pagina principale"""
    return render_template('index.html', models=MODELS)

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint per chat"""
    data = request.json
    message = data.get('message', '')
    model_key = data.get('model', 'gemini')
    
    if not message:
        return jsonify({"success": False, "error": "Messaggio vuoto"})
    
    model_id = MODELS[model_key]['id']
    result = chat_with_ai(message, model_id)
    
    return jsonify(result)

@app.route('/image', methods=['POST'])
def image():
    """Endpoint per analisi immagini"""
    data = request.json
    image_url = data.get('image_url', '')
    prompt = data.get('prompt', 'Descrivi questa immagine')
    model_key = data.get('model', 'gemini')
    
    if not image_url:
        return jsonify({"success": False, "error": "URL immagine mancante"})
    
    model_id = MODELS[model_key]['id']
    result = analyze_image_ai(image_url, prompt, model_id)
    
    return jsonify(result)

@app.route('/models')
def models():
    """Endpoint per lista modelli"""
    return jsonify(MODELS)

if __name__ == '__main__':
    # Crea cartella templates se non esiste
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Avviando l'app...")
    print("🌐 Apri: http://localhost:5000")
    print("✅ API Key configurata")
    print("🤖 Modelli disponibili:")
    for key, model in MODELS.items():
        status = "🆓 GRATUITO" if model['free'] else "💰 A pagamento"
        print(f"   • {model['name']} - {status}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)