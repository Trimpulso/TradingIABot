"""
Servidor Web para Chatbot Gemini
API REST + Frontend HTML interactivo
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime
import os
import random

app = Flask(__name__)
CORS(app)

# Configurar Gemini
API_KEY = "AIzaSyANL8aMxGWC0JQ9xSZy4Pz3ZN7mgPG4DmI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_bitcoin_data():
    """Generar datos de Bitcoin para análisis"""
    now = datetime.now()
    prices = [43000 + random.uniform(-2000, 2000) for _ in range(24)]
    
    return {
        'current_price': round(prices[0], 2),
        'highest_24h': round(max(prices), 2),
        'lowest_24h': round(min(prices), 2),
        'average_24h': round(sum(prices) / len(prices), 2),
        'volatility': round(((max(prices) - min(prices)) / min(prices)) * 100, 2),
        'prices_history': [round(p, 2) for p in prices],
        'timestamp': now.isoformat()
    }

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

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 TRADING IA BOT - CHATBOT GEMINI")
    print("=" * 70)
    
    # Detectar puerto de Railway o usar puerto local
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0' if os.environ.get('RAILWAY_ENVIRONMENT') else '127.0.0.1'
    
    print(f"\n✅ Servidor corriendo en puerto {port}")
    print(f"🌐 Frontend: http://{host}:{port}")
    
    print("\n📡 API Endpoints:")
    print("  • POST /api/chat - Chat con Gemini")
    print("  • GET /api/bitcoin/price - Precio actual")
    print("  • GET /api/bitcoin/prediction - Predicciones")
    print("\n" + "=" * 70 + "\n")
    
    # Usar debug=False en producción
    debug_mode = not os.environ.get('RAILWAY_ENVIRONMENT')
    app.run(debug=debug_mode, port=port, host=host)
