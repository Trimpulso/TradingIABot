#!/usr/bin/env python3
"""
Terminal Chatbot para Trading IA Bot
Interfaz de línea de comandos para interactuar con Gemini
"""

import google.generativeai as genai
from datetime import datetime
import json
import os

# Configurar Gemini
API_KEY = "AIzaSyANL8aMxGWC0JQ9xSZy4Pz3ZN7mgPG4DmI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Mostrar encabezado"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🤖 CHATBOT GEMINI - TRADING IA BOT".center(68) + "║")
    print("║" + "  Análisis de Bitcoin con Inteligencia Artificial".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print(Colors.END)

def print_menu():
    """Mostrar menú de opciones"""
    print(f"\n{Colors.GREEN}{'OPCIONES:':<50}{Colors.END}")
    print(f"  1. {Colors.BLUE}Chat interactivo{Colors.END}")
    print(f"  2. {Colors.BLUE}Análisis rápido de Bitcoin{Colors.END}")
    print(f"  3. {Colors.BLUE}Predicción de precios{Colors.END}")
    print(f"  4. {Colors.BLUE}Recomendaciones de trading{Colors.END}")
    print(f"  5. {Colors.BLUE}Salir{Colors.END}")
    print()

def get_bitcoin_data():
    """Simular datos de Bitcoin"""
    import random
    prices = [random.uniform(42000, 44000) for _ in range(24)]
    return {
        'current': round(prices[0], 2),
        'high_24h': round(max(prices), 2),
        'low_24h': round(min(prices), 2),
        'average_24h': round(sum(prices) / len(prices), 2),
        'volatility': round((max(prices) - min(prices)) / min(prices) * 100, 2)
    }

def chat_with_gemini(user_message, bitcoin_data=None):
    """Enviar mensaje a Gemini"""
    
    if bitcoin_data is None:
        bitcoin_data = get_bitcoin_data()
    
    context = f"""
    Eres un experto en análisis técnico y trading de criptomonedas, especializado en Bitcoin.
    
    DATOS ACTUALES DE BITCOIN:
    - Precio actual: ${bitcoin_data['current']}
    - Máximo 24h: ${bitcoin_data['high_24h']}
    - Mínimo 24h: ${bitcoin_data['low_24h']}
    - Promedio 24h: ${bitcoin_data['average_24h']}
    - Volatilidad: {bitcoin_data['volatility']}%
    - Timestamp: {datetime.now().isoformat()}
    
    INSTRUCCIONES:
    1. Responde siempre en español
    2. Usa análisis técnico profesional
    3. Proporciona números y datos específicos
    4. Incluye recomendaciones claras (COMPRAR/VENDER/ESPERAR)
    5. Siempre advierte sobre los riesgos del trading
    
    Mensaje del usuario: {user_message}
    """
    
    try:
        response = model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=1500
            )
        )
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def interactive_chat():
    """Chat interactivo"""
    print(f"\n{Colors.GREEN}{'CHAT INTERACTIVO':^70}{Colors.END}")
    print(f"{Colors.YELLOW}(Escribe 'salir' para volver al menú){Colors.END}\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input(f"{Colors.BLUE}Tú: {Colors.END}").strip()
            
            if user_input.lower() == 'salir':
                break
            
            if not user_input:
                continue
            
            bitcoin_data = get_bitcoin_data()
            
            print(f"\n{Colors.CYAN}IA: {Colors.END}", end="", flush=True)
            response = chat_with_gemini(user_input, bitcoin_data)
            
            print(response)
            print()
            
            # Guardar en historial
            conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_input,
                'assistant': response,
                'bitcoin_data': bitcoin_data
            })
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Sesión interrumpida.{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
    
    # Guardar conversación
    if conversation_history:
        filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_history, f, ensure_ascii=False, indent=2)
        print(f"{Colors.GREEN}✓ Conversación guardada en: {filename}{Colors.END}")

def quick_bitcoin_analysis():
    """Análisis rápido"""
    bitcoin_data = get_bitcoin_data()
    
    print(f"\n{Colors.GREEN}{'ANÁLISIS RÁPIDO DE BITCOIN':^70}{Colors.END}\n")
    print(f"{Colors.CYAN}Datos actuales:{Colors.END}")
    print(f"  Precio actual:    {Colors.YELLOW}${bitcoin_data['current']:,.2f}{Colors.END}")
    print(f"  Máximo 24h:       {Colors.YELLOW}${bitcoin_data['high_24h']:,.2f}{Colors.END}")
    print(f"  Mínimo 24h:       {Colors.YELLOW}${bitcoin_data['low_24h']:,.2f}{Colors.END}")
    print(f"  Promedio 24h:     {Colors.YELLOW}${bitcoin_data['average_24h']:,.2f}{Colors.END}")
    print(f"  Volatilidad:      {Colors.YELLOW}{bitcoin_data['volatility']:.2f}%{Colors.END}")
    
    print(f"\n{Colors.CYAN}Solicitando análisis de IA...{Colors.END}")
    
    response = chat_with_gemini(
        "Dame un análisis técnico breve de Bitcoin en máximo 150 palabras. "
        "Incluye: tendencia, soporte/resistencia, recomendación (COMPRAR/VENDER/ESPERAR)",
        bitcoin_data
    )
    
    print(f"\n{Colors.CYAN}Análisis:{Colors.END}")
    print(f"{Colors.BOLD}{response}{Colors.END}")

def price_prediction():
    """Predicción de precios"""
    bitcoin_data = get_bitcoin_data()
    
    print(f"\n{Colors.GREEN}{'PREDICCIÓN DE PRECIOS':^70}{Colors.END}\n")
    
    try:
        hours = int(input(f"{Colors.BLUE}¿Para cuántas horas hacia adelante? (1-4): {Colors.END}"))
        hours = max(1, min(4, hours))
    except ValueError:
        hours = 1
    
    print(f"\n{Colors.CYAN}Predicción para {hours} hora(s)...{Colors.END}\n")
    
    response = chat_with_gemini(
        f"Predice el precio máximo y mínimo de Bitcoin para cada una de las próximas {hours} hora(s). "
        f"Actual: ${bitcoin_data['current']}. "
        f"Incluye nivel de confianza para cada predicción. "
        f"Formato: Hora 1: Máximo $X, Mínimo $Y, Confianza Z%",
        bitcoin_data
    )
    
    print(f"{Colors.BOLD}{response}{Colors.END}")

def trading_recommendations():
    """Recomendaciones de trading"""
    bitcoin_data = get_bitcoin_data()
    
    print(f"\n{Colors.GREEN}{'RECOMENDACIONES DE TRADING':^70}{Colors.END}\n")
    print(f"{Colors.CYAN}Solicitando recomendaciones profesionales...{Colors.END}\n")
    
    response = chat_with_gemini(
        "Basándote en los datos actuales de Bitcoin, dame:"
        "1. Recomendación: COMPRAR/VENDER/ESPERAR"
        "2. Precio de entrada sugerido"
        "3. Stop loss sugerido"
        "4. Objetivo de ganancias (Take Profit)"
        "5. Nivel de riesgo (BAJO/MEDIO/ALTO)"
        "6. Argumento principal para la recomendación",
        bitcoin_data
    )
    
    print(f"{Colors.BOLD}{response}{Colors.END}")

def main():
    """Función principal"""
    print_header()
    
    print(f"{Colors.YELLOW}Iniciando conexión con Gemini AI...{Colors.END}")
    
    try:
        # Prueba de conexión
        test = model.generate_content("Hola", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
        print(f"{Colors.GREEN}✓ Conexión establecida correctamente{Colors.END}\n")
    except Exception as e:
        print(f"{Colors.RED}❌ Error de conexión: {str(e)}{Colors.END}")
        return
    
    while True:
        print_menu()
        
        try:
            choice = input(f"{Colors.BLUE}Selecciona una opción (1-5): {Colors.END}").strip()
            
            if choice == '1':
                interactive_chat()
            elif choice == '2':
                quick_bitcoin_analysis()
            elif choice == '3':
                price_prediction()
            elif choice == '4':
                trading_recommendations()
            elif choice == '5':
                print(f"\n{Colors.GREEN}¡Hasta luego! 👋{Colors.END}\n")
                break
            else:
                print(f"{Colors.RED}❌ Opción no válida. Intenta de nuevo.{Colors.END}")
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Programa interrumpido por el usuario.{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.END}")

if __name__ == "__main__":
    main()
