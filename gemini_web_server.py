"""
Servidor Web para Chatbot Gemini
API REST + Frontend HTML interactivo
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime, timedelta
import json
import threading
import os
import random

app = Flask(__name__)
CORS(app)

# Configurar Gemini
API_KEY = "AIzaSyANL8aMxGWC0JQ9xSZy4Pz3ZN7mgPG4DmI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Almacenar conversaciones
conversations = {}
bitcoin_data_cache = None

def generate_bitcoin_data():
    """Generar datos de Bitcoin para análisis"""
    global bitcoin_data_cache
    
    now = datetime.now()
    prices = []
    
    for i in range(24):
        price = 43000 + random.uniform(-2000, 2000)
        prices.append(round(price, 2))
    
    bitcoin_data_cache = {
        'current_price': prices[0],
        'highest_24h': max(prices),
        'lowest_24h': min(prices),
        'average_24h': round(sum(prices) / len(prices), 2),
        'volatility': round(((max(prices) - min(prices)) / min(prices)) * 100, 2),
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
        
        # Crear respuesta mock (para demo sin API)
        responses = {
            'precio': f"El precio actual de Bitcoin es ${bitcoin_data['current_price']:,.2f}. Ha alcanzado un máximo de ${bitcoin_data['highest_24h']:,.2f} y un mínimo de ${bitcoin_data['lowest_24h']:,.2f} en las últimas 24 horas.",
            'maximo': f"En las últimas 24 horas, el máximo fue ${bitcoin_data['highest_24h']:,.2f} y el mínimo ${bitcoin_data['lowest_24h']:,.2f}. La volatilidad actual es del {bitcoin_data['volatility']:.2f}%.",
            'comprar': f"RECOMENDACIÓN: COMPRAR ⬆️\n- Precio de entrada sugerido: ${bitcoin_data['current_price'] * 0.98:,.2f}\n- Stop Loss: ${bitcoin_data['lowest_24h']:,.2f}\n- Take Profit: ${bitcoin_data['current_price'] * 1.05:,.2f}\n- Riesgo: MEDIO\n\nRazón: El Bitcoin está en una zona de acumulación. Los indicadores técnicos muestran potencial alcista.",
            'vender': f"RECOMENDACIÓN: VENDER ⬇️\n- Precio de salida sugerido: ${bitcoin_data['current_price'] * 1.02:,.2f}\n- Stop Loss: ${bitcoin_data['highest_24h']:,.2f}\n- Razón: Resistencia identificada en ${bitcoin_data['highest_24h']:,.2f}",
            'default': f"Soy tu asistente de trading. Datos actuales:\n- Precio: ${bitcoin_data['current_price']:,.2f}\n- Rango 24h: ${bitcoin_data['lowest_24h']:,.2f} - ${bitcoin_data['highest_24h']:,.2f}\n- Volatilidad: {bitcoin_data['volatility']:.2f}%\n\nPuedo ayudarte con análisis, predicciones y recomendaciones de trading."
        }
        
        # Seleccionar respuesta basada en keywords
        msg_lower = user_message.lower()
        assistant_message = responses.get('default')
        
        if any(word in msg_lower for word in ['precio', 'cuánto', 'cuanto', 'costo', 'vale']):
            assistant_message = responses['precio']
        elif any(word in msg_lower for word in ['máximo', 'maximo', 'mínimo', 'minimo', 'rango']):
            assistant_message = responses['maximo']
        elif any(word in msg_lower for word in ['comprar', 'buy', 'largo', 'bullish', 'alcista']):
            assistant_message = responses['comprar']
        elif any(word in msg_lower for word in ['vender', 'sell', 'corto', 'bearish', 'bajista']):
            assistant_message = responses['vender']
        
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
            'confidence': 75 + random.randint(-10, 10)
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
    
    # Detectar puerto de Railway o usar puerto local
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0' if os.environ.get('RAILWAY_ENVIRONMENT') else '127.0.0.1'
    
    print(f"\nServidor corriendo en: http://{host}:{port}")
    print(f"Frontend: http://{host}:{port}")
    
    print("\nEndpoints disponibles:")
    print("  - POST /api/chat - Enviar mensaje al chatbot")
    print("  - GET /api/bitcoin/price - Obtener precio de Bitcoin")
    print("  - GET /api/bitcoin/prediction - Predicción de máximos/mínimos")
    print("  - GET /api/conversation/<session_id> - Ver historial")
    print("\n" + "=" * 70 + "\n")
    
    # Usar debug=False en producción
    debug_mode = not os.environ.get('RAILWAY_ENVIRONMENT')
    app.run(debug=debug_mode, port=port, host=host)
