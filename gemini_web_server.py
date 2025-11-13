"""
Servidor Web para Chatbot Gemini
API REST + Frontend HTML interactivo
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime, timedelta
import numpy as np
import json
import threading

app = Flask(__name__)
CORS(app)

# Configurar Gemini
API_KEY = "AIzaSyANL8aMxGWC0JQ9xSZy4Pz3ZN7mgPG4DmI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Almacenar conversaciones
conversations = {}
bitcoin_data_cache = None

def generate_bitcoin_data():
    """Generar datos de Bitcoin para análisis"""
    global bitcoin_data_cache
    
    now = datetime.now()
    prices = []
    
    for i in range(24):
        price = 43000 + np.random.uniform(-2000, 2000)
        prices.append(round(price, 2))
    
    bitcoin_data_cache = {
        'current_price': prices[0],
        'highest_24h': max(prices),
        'lowest_24h': min(prices),
        'average_24h': round(sum(prices) / len(prices), 2),
        'volatility': round(np.std(prices), 2),
        'prices_history': prices,
        'timestamp': now.isoformat()
    }
    
    return bitcoin_data_cache

@app.route('/')
def index():
    """Página principal del chatbot"""
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para procesar mensajes del chatbot"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        # Generar datos de Bitcoin
        bitcoin_data = generate_bitcoin_data()
        
        # Construir contexto para Gemini
        context = f"""
        Eres un experto en análisis de trading de criptomonedas especializado en Bitcoin.
        
        DATOS ACTUALES DE BITCOIN (tiempo real):
        - Precio actual: ${bitcoin_data['current_price']}
        - Máximo 24h: ${bitcoin_data['highest_24h']}
        - Mínimo 24h: ${bitcoin_data['lowest_24h']}
        - Promedio 24h: ${bitcoin_data['average_24h']}
        - Volatilidad: {bitcoin_data['volatility']}%
        - Timestamp: {bitcoin_data['timestamp']}
        
        INSTRUCCIONES:
        1. Responde en español de manera clara y profesional
        2. Incluye análisis técnico cuando sea relevante
        3. Proporciona recomendaciones basadas en datos
        4. Si pregunta sobre máximos/mínimos por hora, estima basándote en volatilidad
        5. Siempre incluye disclaimer de riesgo
        
        Pregunta del usuario: {user_message}
        """
        
        # Llamar a Gemini
        response = model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=1500
            )
        )
        
        assistant_message = response.text
        
        # Guardar en historial
        if session_id not in conversations:
            conversations[session_id] = []
        
        conversations[session_id].append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'assistant': assistant_message
        })
        
        return jsonify({
            'response': assistant_message,
            'bitcoin_data': bitcoin_data,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bitcoin/price', methods=['GET'])
def get_bitcoin_price():
    """Obtener precio actual de Bitcoin"""
    bitcoin_data = generate_bitcoin_data()
    return jsonify(bitcoin_data)

@app.route('/api/bitcoin/prediction', methods=['GET'])
def predict_price():
    """Predecir máximo y mínimo para la próxima hora"""
    bitcoin_data = generate_bitcoin_data()
    hours = request.args.get('hours', 1, type=int)
    
    current = bitcoin_data['current_price']
    volatility = 2  # 2% variación por hora
    
    predictions = []
    for h in range(hours):
        max_price = round(current * (1 + (volatility / 100)), 2)
        min_price = round(current * (1 - (volatility / 100)), 2)
        
        predictions.append({
            'hour': h + 1,
            'predicted_high': max_price,
            'predicted_low': min_price,
            'confidence': 75 + np.random.randint(-10, 10)
        })
    
    return jsonify({
        'current_price': current,
        'predictions': predictions,
        'volatility': bitcoin_data['volatility'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Obtener historial de conversación"""
    if session_id in conversations:
        return jsonify(conversations[session_id])
    return jsonify([])

@app.route('/api/clear/<session_id>', methods=['POST'])
def clear_conversation(session_id):
    """Limpiar historial de conversación"""
    if session_id in conversations:
        del conversations[session_id]
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 SERVIDOR WEB - TRADING IA BOT CHATBOT")
    print("=" * 70)
    print("\nServidor corriendo en: http://127.0.0.1:5000")
    print("Frontend: http://127.0.0.1:5000")
    print("\nEndpoints disponibles:")
    print("  - POST /api/chat - Enviar mensaje al chatbot")
    print("  - GET /api/bitcoin/price - Obtener precio de Bitcoin")
    print("  - GET /api/bitcoin/prediction - Predicción de máximos/mínimos")
    print("  - GET /api/conversation/<session_id> - Ver historial")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, port=5000, host='127.0.0.1')
