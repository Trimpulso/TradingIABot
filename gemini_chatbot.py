"""
Chatbot AI con Gemini - Trading IA Bot
Análisis de Bitcoin en tiempo real
Predicciones de máximos y mínimos por hora
"""

import os
import sys
import json
from datetime import datetime, timedelta
import google.generativeai as genai
import pandas as pd
import numpy as np

# Configurar API Key
API_KEY = "AIzaSyANL8aMxGWC0JQ9xSZy4Pz3ZN7mgPG4DmI"
genai.configure(api_key=API_KEY)

class TradingChatbot:
    def __init__(self):
        """Inicializar chatbot con Gemini"""
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat_history = []
        self.trading_data = {}
        
    def generate_mock_bitcoin_data(self):
        """Generar datos mock de Bitcoin para demostración"""
        now = datetime.now()
        data = []
        
        # Generar datos para últimas 24 horas
        for i in range(24):
            timestamp = now - timedelta(hours=i)
            # Bitcoin fluctúa entre 42000 y 45000 USD
            price = np.random.uniform(42000, 45000)
            volume = np.random.uniform(1000, 5000)
            
            data.append({
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'price': round(price, 2),
                'volume': round(volume, 2),
                'change_percent': round(np.random.uniform(-2, 2), 2)
            })
        
        return data
    
    def analyze_bitcoin(self):
        """Analizar datos de Bitcoin"""
        data = self.generate_mock_bitcoin_data()
        
        prices = [d['price'] for d in data]
        
        analysis = {
            'current_price': round(prices[0], 2),
            'highest_24h': round(max(prices), 2),
            'lowest_24h': round(min(prices), 2),
            'average_24h': round(sum(prices) / len(prices), 2),
            'volatility': round(np.std(prices), 2),
            'trend': 'ALCISTA' if prices[0] > prices[-1] else 'BAJISTA',
            'recommendation': self._get_recommendation(prices),
            'data_points': data[:6]  # Últimas 6 horas
        }
        
        return analysis
    
    def _get_recommendation(self, prices):
        """Generar recomendación basada en precios"""
        if prices[0] > prices[-1]:
            return 'COMPRA - Tendencia alcista detectada'
        else:
            return 'VENTA - Tendencia bajista detectada'
    
    def chat(self, user_message):
        """Procesar mensajes del usuario con Gemini"""
        
        # Obtener datos de Bitcoin
        bitcoin_analysis = self.analyze_bitcoin()
        
        # Construir contexto para Gemini
        context = f"""
        Eres un experto en análisis de trading de criptomonedas.
        
        DATOS ACTUALES DE BITCOIN:
        - Precio actual: ${bitcoin_analysis['current_price']}
        - Máximo 24h: ${bitcoin_analysis['highest_24h']}
        - Mínimo 24h: ${bitcoin_analysis['lowest_24h']}
        - Promedio 24h: ${bitcoin_analysis['average_24h']}
        - Volatilidad: ${bitcoin_analysis['volatility']}
        - Tendencia: {bitcoin_analysis['trend']}
        - Recomendación: {bitcoin_analysis['recommendation']}
        
        Responde en español de manera clara y profesional.
        Incluye análisis técnico cuando sea relevante.
        Proporciona recomendaciones basadas en datos.
        """
        
        # Llamar a Gemini con caché
        try:
            response = self.model.generate_content(
                [context, user_message],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.9,
                    max_output_tokens=1000
                )
            )
            
            assistant_message = response.text
            
            # Guardar en historial
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_message,
                'assistant': assistant_message,
                'bitcoin_data': bitcoin_analysis
            })
            
            return {
                'response': assistant_message,
                'bitcoin_data': bitcoin_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'response': f'Error: {str(e)}',
                'bitcoin_data': bitcoin_analysis
            }
    
    def get_price_prediction(self, hours=1):
        """Predecir precio máximo y mínimo para las próximas horas"""
        data = self.generate_mock_bitcoin_data()
        current_price = data[0]['price']
        
        # Simular predicción
        volatility = 2  # 2% de variación máxima
        predicted_high = round(current_price * (1 + volatility/100), 2)
        predicted_low = round(current_price * (1 - volatility/100), 2)
        
        prompt = f"""
        Basándote en el análisis técnico de Bitcoin:
        - Precio actual: ${current_price}
        - Predicción máximo próxima hora: ${predicted_high}
        - Predicción mínimo próxima hora: ${predicted_low}
        
        ¿Cuál es tu análisis? ¿Debo comprar, vender o esperar?
        Incluye riesgo/recompensa esperado.
        """
        
        return self.chat(prompt)
    
    def start_interactive_chat(self):
        """Iniciar chat interactivo con el usuario"""
        print("=" * 70)
        print("🤖 TRADING IA BOT - CHATBOT CON GEMINI")
        print("=" * 70)
        print("\nAnálisis de Bitcoin en tiempo real")
        print("Escribe tus preguntas o 'salir' para terminar\n")
        
        while True:
            user_input = input("\n💬 Tú: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("\n¡Hasta luego! 👋")
                break
            
            if not user_input:
                continue
            
            print("\n⏳ Analizando...")
            result = self.chat(user_input)
            
            print(f"\n🤖 Gemini: {result['response']}")
            print(f"\n📊 Datos Bitcoin:")
            print(f"   • Precio: ${result['bitcoin_data']['current_price']}")
            print(f"   • Máximo 24h: ${result['bitcoin_data']['highest_24h']}")
            print(f"   • Mínimo 24h: ${result['bitcoin_data']['lowest_24h']}")
            print(f"   • Tendencia: {result['bitcoin_data']['trend']}")
            print(f"   • Volatilidad: {result['bitcoin_data']['volatility']}%")
    
    def save_conversation(self, filename='chatbot_history.json'):
        """Guardar historial de conversación"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Conversación guardada en: {filename}")
    
    def get_summary(self):
        """Obtener resumen de la sesión"""
        return {
            'total_messages': len(self.chat_history),
            'start_time': self.chat_history[0]['timestamp'] if self.chat_history else None,
            'end_time': self.chat_history[-1]['timestamp'] if self.chat_history else None,
            'history': self.chat_history
        }


def main():
    """Función principal"""
    chatbot = TradingChatbot()
    
    print("\n" + "=" * 70)
    print("🚀 TRADING IA BOT - CHATBOT CON GEMINI 1.5 FLASH")
    print("=" * 70)
    
    print("\nOpciones:")
    print("1. Chat interactivo")
    print("2. Predicción de precio (próxima hora)")
    print("3. Análisis rápido de Bitcoin")
    print("4. Salir")
    
    choice = input("\nElige una opción (1-4): ").strip()
    
    if choice == '1':
        chatbot.start_interactive_chat()
    elif choice == '2':
        print("\n⏳ Generando predicción...")
        result = chatbot.get_price_prediction()
        print(f"\n🔮 Predicción: {result['response']}")
        print(f"\n📊 Datos: {json.dumps(result['bitcoin_data'], indent=2, ensure_ascii=False)}")
    elif choice == '3':
        data = chatbot.analyze_bitcoin()
        print("\n📊 ANÁLISIS DE BITCOIN")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("Adiós! 👋")
        return
    
    # Guardar conversación si hay
    if chatbot.chat_history:
        chatbot.save_conversation()


if __name__ == "__main__":
    main()
