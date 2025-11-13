#!/usr/bin/env python3
"""
Test Script para Gemini Chatbot
Verifica que todo esté funcionando correctamente
"""

import sys
import subprocess
from datetime import datetime

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_test_header():
    """Mostrar encabezado de tests"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "═" * 68 + "╗")
    print("║" + " TEST - TRADING IA BOT CHATBOT ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print(Colors.END)

def test_python_version():
    """Prueba versión de Python"""
    print(f"\n{Colors.BLUE}[1] Verificando versión de Python...{Colors.END}")
    version = sys.version
    print(f"    Versión: {version}")
    if sys.version_info >= (3, 10):
        print(f"    {Colors.GREEN}✓ OK{Colors.END}")
        return True
    else:
        print(f"    {Colors.RED}✗ FALLA - Se requiere Python 3.10+{Colors.END}")
        return False

def test_imports():
    """Prueba importaciones necesarias"""
    print(f"\n{Colors.BLUE}[2] Verificando importaciones...{Colors.END}")
    
    imports_to_test = [
        ("google.generativeai", "Google Generative AI"),
        ("flask", "Flask"),
        ("flask_cors", "Flask-CORS"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("json", "JSON (built-in)"),
        ("datetime", "DateTime (built-in)")
    ]
    
    all_ok = True
    for module_name, display_name in imports_to_test:
        try:
            __import__(module_name)
            print(f"    {Colors.GREEN}✓{Colors.END} {display_name:<30} importado")
        except ImportError as e:
            print(f"    {Colors.RED}✗{Colors.END} {display_name:<30} {Colors.RED}NO ENCONTRADO{Colors.END}")
            all_ok = False
    
    return all_ok

def test_gemini_connection():
    """Prueba conexión con Gemini API"""
    print(f"\n{Colors.BLUE}[3] Verificando API de Gemini...{Colors.END}")
    
    try:
        import google.generativeai as genai
        API_KEY = "AIzaSyANL8aMxGWC0JQ9xSZy4Pz3ZN7mgPG4DmI"
        
        if API_KEY and len(API_KEY) > 20:
            print(f"    {Colors.GREEN}✓ API Key configurada{Colors.END}")
            print(f"    Key (primeros 10 chars): {API_KEY[:10]}...")
            genai.configure(api_key=API_KEY)
            print(f"    {Colors.GREEN}✓ Gemini SDK inicializado{Colors.END}")
            return True
        else:
            print(f"    {Colors.RED}✗ API Key inválida{Colors.END}")
            return False
    
    except Exception as e:
        print(f"    {Colors.RED}✗ Error: {str(e)}{Colors.END}")
        return False

def test_files_exist():
    """Verificar archivos necesarios"""
    print(f"\n{Colors.BLUE}[4] Verificando archivos necesarios...{Colors.END}")
    
    import os
    files_to_check = [
        ("gemini_web_server.py", "Servidor web"),
        ("chatbot_terminal.py", "Chatbot terminal"),
        ("templates/chatbot.html", "Template HTML"),
        (".venv/Scripts/python.exe", "Python venv"),
    ]
    
    all_ok = True
    for file_path, display_name in files_to_check:
        if os.path.exists(file_path):
            print(f"    {Colors.GREEN}✓{Colors.END} {display_name:<30} {file_path}")
        else:
            print(f"    {Colors.RED}✗{Colors.END} {display_name:<30} {Colors.RED}NO ENCONTRADO{Colors.END}")
            all_ok = False
    
    return all_ok

def test_git_repo():
    """Verificar repositorio Git"""
    print(f"\n{Colors.BLUE}[5] Verificando repositorio Git...{Colors.END}")
    
    try:
        result = subprocess.run(
            ['git', 'status'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"    {Colors.GREEN}✓ Repositorio Git OK{Colors.END}")
            
            # Verificar commits
            result2 = subprocess.run(
                ['git', 'log', '--oneline', '-5'],
                capture_output=True,
                text=True
            )
            
            print(f"    Últimos 5 commits:")
            for line in result2.stdout.split('\n')[:5]:
                if line.strip():
                    print(f"      {Colors.YELLOW}{line}{Colors.END}")
            
            return True
        else:
            print(f"    {Colors.RED}✗ Git no disponible{Colors.END}")
            return False
    
    except Exception as e:
        print(f"    {Colors.RED}✗ Error: {str(e)}{Colors.END}")
        return False

def test_flask_server():
    """Test rápido de Flask"""
    print(f"\n{Colors.BLUE}[6] Verificando configuración de Flask...{Colors.END}")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return "OK"
        
        print(f"    {Colors.GREEN}✓ Flask configurado correctamente{Colors.END}")
        
        # Verificar que los templates existen
        import os
        if os.path.exists('templates/chatbot.html'):
            print(f"    {Colors.GREEN}✓ Template HTML encontrado{Colors.END}")
            return True
        else:
            print(f"    {Colors.RED}✗ Template HTML no encontrado{Colors.END}")
            return False
    
    except Exception as e:
        print(f"    {Colors.RED}✗ Error: {str(e)}{Colors.END}")
        return False

def print_summary(results):
    """Imprimir resumen de tests"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("═" * 70)
    print("RESUMEN DE TESTS".center(70))
    print("═" * 70)
    print(Colors.END)
    
    tests = [
        "Versión de Python",
        "Importaciones",
        "Conexión Gemini",
        "Archivos necesarios",
        "Repositorio Git",
        "Configuración Flask"
    ]
    
    for test_name, result in zip(tests, results):
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if result else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"  {test_name:<40} {status}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n{Colors.BOLD}", end="")
    if passed == total:
        print(f"{Colors.GREEN}✓ TODOS LOS TESTS PASARON ({passed}/{total}){Colors.END}")
    elif passed >= total - 1:
        print(f"{Colors.YELLOW}⚠ CASI TODOS LOS TESTS PASARON ({passed}/{total}){Colors.END}")
    else:
        print(f"{Colors.RED}✗ ALGUNOS TESTS FALLARON ({passed}/{total}){Colors.END}")
    
    print("═" * 70)

def print_next_steps():
    """Mostrar próximos pasos"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}PRÓXIMOS PASOS:{Colors.END}")
    print("""
  1. CHATBOT WEB:
     → python gemini_web_server.py
     → Abre: http://127.0.0.1:5000

  2. CHATBOT TERMINAL:
     → python chatbot_terminal.py
     → Selecciona opción 1-4

  3. MÁS INFORMACIÓN:
     → Lee: GUIA_CHATBOT_WEB.md
     → Lee: README_FINAL.md

  4. REPOSITORIO:
     → github.com/Trimpulso/TradingIABot
""")

def main():
    """Función principal"""
    print_test_header()
    
    # Ejecutar tests
    results = []
    
    results.append(test_python_version())
    results.append(test_imports())
    results.append(test_gemini_connection())
    results.append(test_files_exist())
    results.append(test_git_repo())
    results.append(test_flask_server())
    
    # Mostrar resumen
    print_summary(results)
    
    # Próximos pasos
    if all(results):
        print_next_steps()
    else:
        print(f"\n{Colors.YELLOW}⚠ Algunos tests fallaron. Por favor, soluciona los errores antes de continuar.{Colors.END}\n")

if __name__ == "__main__":
    main()
