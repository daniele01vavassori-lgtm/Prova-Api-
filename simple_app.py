#!/usr/bin/env python3
"""
App Web Semplice per testare OpenRouter API
"""

from flask import Flask
import requests

app = Flask(__name__)

# La tua API Key
API_KEY = "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"

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🤖 OpenRouter AI Tester</title>
    <meta charset="UTF-8">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { 
            color: #333; 
            text-align: center;
            margin-bottom: 30px;
        }
        .status { 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px;
            font-weight: bold;
        }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .test-section {
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #dee2e6;
        }
        textarea, input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        button:hover { transform: translateY(-2px); }
        .response {
            background: #fff;
            border: 2px solid #28a745;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 OpenRouter AI Tester</h1>
        
        <div class="status success">
            ✅ API Key Configurata: sk-or-v1-...c9c10
        </div>
        
        <div class="status info">
            🌟 Modelli Disponibili: Gemini (GRATUITO), GPT, Claude, Llama
        </div>
        
        <div class="test-section">
            <h3>💬 Test Chat con Gemini</h3>
            <textarea id="message" placeholder="Scrivi il tuo messaggio qui..." rows="3">Ciao! Puoi dirmi 3 curiosità sull'intelligenza artificiale?</textarea>
            <button onclick="testChat()">🚀 Invia a Gemini</button>
            <div id="chatResponse"></div>
        </div>
        
        <div class="test-section">
            <h3>👁️ Test Analisi Immagine</h3>
            <input type="url" id="imageUrl" placeholder="URL dell'immagine" 
                   value="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg">
            <input type="text" id="imagePrompt" placeholder="Cosa vuoi sapere?" value="Descrivi questa immagine">
            <button onclick="testImage()">👁️ Analizza con Gemini Vision</button>
            <div id="imageResponse"></div>
        </div>
        
        <div class="test-section">
            <h3>🔧 Test Rapido API</h3>
            <button onclick="quickTest()">⚡ Test Veloce</button>
            <div id="quickResponse"></div>
        </div>
    </div>

    <script>
        async function testChat() {
            const message = document.getElementById('message').value;
            const responseDiv = document.getElementById('chatResponse');
            
            responseDiv.innerHTML = '🤖 Pensando...';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    responseDiv.innerHTML = `<div class="response">🤖 Gemini: ${result.message}</div>`;
                } else {
                    responseDiv.innerHTML = `<div style="color: red;">❌ ${result.error}</div>`;
                }
            } catch (error) {
                responseDiv.innerHTML = `<div style="color: red;">❌ Errore: ${error.message}</div>`;
            }
        }
        
        async function testImage() {
            const imageUrl = document.getElementById('imageUrl').value;
            const prompt = document.getElementById('imagePrompt').value;
            const responseDiv = document.getElementById('imageResponse');
            
            responseDiv.innerHTML = '👁️ Analizzando...';
            
            try {
                const response = await fetch('/api/image', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image_url: imageUrl, prompt: prompt })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    responseDiv.innerHTML = `<div class="response">👁️ Gemini vede: ${result.message}</div>`;
                } else {
                    responseDiv.innerHTML = `<div style="color: red;">❌ ${result.error}</div>`;
                }
            } catch (error) {
                responseDiv.innerHTML = `<div style="color: red;">❌ Errore: ${error.message}</div>`;
            }
        }
        
        async function quickTest() {
            const responseDiv = document.getElementById('quickResponse');
            responseDiv.innerHTML = '⚡ Testando...';
            
            try {
                const response = await fetch('/api/test');
                const result = await response.json();
                
                if (result.success) {
                    responseDiv.innerHTML = `<div class="response">✅ ${result.message}</div>`;
                } else {
                    responseDiv.innerHTML = `<div style="color: red;">❌ ${result.error}</div>`;
                }
            } catch (error) {
                responseDiv.innerHTML = `<div style="color: red;">❌ Errore: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>
    '''

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        from flask import request, jsonify
        data = request.json
        message = data.get('message', '')
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-2.5-flash-lite",
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 300
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "success": True,
                "message": result['choices'][0]['message']['content']
            })
        else:
            return jsonify({
                "success": False,
                "error": f"API Error: {response.status_code}"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/image', methods=['POST'])
def api_image():
    try:
        from flask import request, jsonify
        data = request.json
        image_url = data.get('image_url', '')
        prompt = data.get('prompt', 'Descrivi questa immagine')
        
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
                }],
                "max_tokens": 300
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "success": True,
                "message": result['choices'][0]['message']['content']
            })
        else:
            return jsonify({
                "success": False,
                "error": f"API Error: {response.status_code}"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/test')
def api_test():
    try:
        from flask import jsonify
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json().get('data', [])
            return jsonify({
                "success": True,
                "message": f"API Key funziona! {len(models)} modelli disponibili."
            })
        else:
            return jsonify({
                "success": False,
                "error": f"API Error: {response.status_code}"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    print("🚀 Avviando l'app semplice...")
    print("🌐 Apri: http://localhost:8080")
    print("✅ API Key configurata")
    app.run(host='0.0.0.0', port=8080, debug=True)