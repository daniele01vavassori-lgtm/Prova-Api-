#!/usr/bin/env python3
"""
Server veloce per cellulare - Demo OpenRouter AI
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests

# La tua API Key
API_KEY = "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"

class MobileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/demo':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 OpenRouter AI Mobile</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 10px;
        }}
        .container {{
            max-width: 100%;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{ font-size: 1.8em; margin-bottom: 5px; }}
        .status {{
            padding: 15px;
            background: #d4edda;
            color: #155724;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
        }}
        .section {{
            padding: 20px;
            border-bottom: 1px solid #eee;
        }}
        .section h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        textarea, input {{
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
        }}
        textarea {{ min-height: 80px; resize: vertical; }}
        .btn {{
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px 0;
            touch-action: manipulation;
        }}
        .btn:active {{ transform: scale(0.98); }}
        .response {{
            background: #f8f9fa;
            border: 2px solid #28a745;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
            line-height: 1.5;
            font-size: 14px;
        }}
        .loading {{
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 20px;
        }}
        .error {{
            background: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }}
        .spinner {{
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 10px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .feature {{
            background: white;
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
        }}
        .feature h4 {{ color: #333; margin-bottom: 8px; }}
        .feature p {{ color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 OpenRouter AI</h1>
            <p>Demo Mobile per la tua API Key</p>
        </div>
        
        <div class="status">
            ✅ API Key Attiva | 🆓 Gemini Gratuito | 👁️ Vision AI
        </div>
        
        <div class="section">
            <h3>💬 Chat con Gemini</h3>
            <textarea id="chatMessage" placeholder="Scrivi qui il tuo messaggio...">Ciao! Dimmi 3 curiosità sull'AI</textarea>
            <button class="btn" onclick="testChat()">🚀 Invia a Gemini</button>
            <div id="chatResponse"></div>
        </div>
        
        <div class="section">
            <h3>👁️ Analisi Immagine</h3>
            <input type="url" id="imageUrl" placeholder="URL immagine" 
                   value="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg">
            <input type="text" id="imagePrompt" placeholder="Cosa vuoi sapere?" value="Descrivi questa immagine">
            <button class="btn" onclick="testVision()">👁️ Analizza con Gemini Vision</button>
            <div id="visionResponse"></div>
        </div>
        
        <div class="section">
            <h3>🎯 Modelli Disponibili</h3>
            <div class="feature">
                <h4>🧠 Gemini 2.5 Flash Lite</h4>
                <p><strong>GRATUITO</strong> - Veloce e potente</p>
            </div>
            <div class="feature">
                <h4>🤖 GPT-3.5 Turbo</h4>
                <p><strong>A pagamento</strong> - Veloce ed economico</p>
            </div>
            <div class="feature">
                <h4>🔥 Claude 3.7 Sonnet</h4>
                <p><strong>A pagamento</strong> - Eccellente per scrittura</p>
            </div>
        </div>
        
        <div class="section">
            <h3>🚀 Per la Tua App</h3>
            <button class="btn" onclick="showCode()">📋 Mostra Codice Python</button>
            <div id="codeSection" style="display: none;">
                <textarea readonly style="font-family: monospace; font-size: 12px; height: 200px;">import requests

def chat_with_ai(message):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={{
            "Authorization": "Bearer {API_KEY}",
            "Content-Type": "application/json"
        }},
        json={{
            "model": "google/gemini-2.5-flash-lite",
            "messages": [{{"role": "user", "content": message}}]
        }}
    )
    return response.json()['choices'][0]['message']['content']

# Usa così:
risposta = chat_with_ai("Ciao!")
print(risposta)</textarea>
            </div>
        </div>
    </div>

    <script>
        const API_KEY = "{API_KEY}";
        
        async function testChat() {{
            const message = document.getElementById('chatMessage').value;
            const responseDiv = document.getElementById('chatResponse');
            
            if (!message.trim()) {{
                alert('Scrivi un messaggio!');
                return;
            }}
            
            responseDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Gemini sta pensando...</div>';
            
            try {{
                const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {{
                    method: 'POST',
                    headers: {{
                        'Authorization': `Bearer ${{API_KEY}}`,
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        model: 'google/gemini-2.5-flash-lite',
                        messages: [{{ role: 'user', content: message }}],
                        max_tokens: 300
                    }})
                }});
                
                if (response.ok) {{
                    const result = await response.json();
                    const aiMessage = result.choices[0].message.content;
                    responseDiv.innerHTML = `<div class="response">🤖 <strong>Gemini:</strong><br><br>${{aiMessage}}</div>`;
                }} else if (response.status === 429) {{
                    responseDiv.innerHTML = '<div class="response error">⚠️ Rate limit. Aspetta 10 secondi.</div>';
                }} else {{
                    responseDiv.innerHTML = `<div class="response error">❌ Errore: ${{response.status}}</div>`;
                }}
            }} catch (error) {{
                responseDiv.innerHTML = `<div class="response error">❌ Errore: ${{error.message}}</div>`;
            }}
        }}
        
        async function testVision() {{
            const imageUrl = document.getElementById('imageUrl').value;
            const prompt = document.getElementById('imagePrompt').value;
            const responseDiv = document.getElementById('visionResponse');
            
            if (!imageUrl.trim()) {{
                alert('Inserisci URL immagine!');
                return;
            }}
            
            responseDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Analizzando immagine...</div>';
            
            try {{
                const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {{
                    method: 'POST',
                    headers: {{
                        'Authorization': `Bearer ${{API_KEY}}`,
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        model: 'google/gemini-2.5-flash-lite',
                        messages: [{{
                            role: 'user',
                            content: [
                                {{ type: 'text', text: prompt }},
                                {{ type: 'image_url', image_url: {{ url: imageUrl }} }}
                            ]
                        }}],
                        max_tokens: 300
                    }})
                }});
                
                if (response.ok) {{
                    const result = await response.json();
                    const aiMessage = result.choices[0].message.content;
                    responseDiv.innerHTML = `<div class="response">👁️ <strong>Gemini Vision:</strong><br><br>${{aiMessage}}</div>`;
                }} else {{
                    responseDiv.innerHTML = `<div class="response error">❌ Errore: ${{response.status}}</div>`;
                }}
            }} catch (error) {{
                responseDiv.innerHTML = `<div class="response error">❌ Errore: ${{error.message}}</div>`;
            }}
        }}
        
        function showCode() {{
            const codeSection = document.getElementById('codeSection');
            codeSection.style.display = codeSection.style.display === 'none' ? 'block' : 'none';
        }}
    </script>
</body>
</html>
            '''
            
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    port = 9000
    server = HTTPServer(('0.0.0.0', port), MobileHandler)
    print(f"🚀 Server mobile avviato!")
    print(f"📱 Apri sul cellulare: http://localhost:{port}")
    print(f"🌐 O usa l'IP del computer: http://[IP-DEL-TUO-PC]:{port}")
    print(f"✅ API Key configurata")
    print(f"🤖 Gemini GRATUITO attivo")
    print("=" * 50)
    server.serve_forever()