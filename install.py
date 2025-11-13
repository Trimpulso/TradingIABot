#!/usr/bin/env python3
"""
Script de instalación y verificación de Trading IA Bot
Ejecutar: python install.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    """Imprimir encabezado."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step_num, text):
    """Imprimir paso."""
    print(f"  [{step_num}] {text}")

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado."""
    try:
        print(f"  ⏳ {description}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ {description}")
            return True
        else:
            print(f"  ✗ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Ejecutar instalación."""
    
    print_header("🤖 TRADING IA BOT - INSTALADOR")
    
    # Verificar Python
    print_step(1, "Verificando Python")
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  Python: {python_version}")
    if sys.version_info < (3, 8):
        print("  ✗ Se requiere Python 3.8+")
        sys.exit(1)
    print(f"  ✓ Python {python_version} OK\n")
    
    # Crear .env
    print_step(2, "Configurar .env")
    env_path = Path(".env")
    if not env_path.exists():
        print("  ⏳ Creando .env...")
        run_command("copy .env.example .env" if os.name == 'nt' else "cp .env.example .env", 
                   "Copiar .env")
        print("  ⚠️  Edita .env con tus credenciales de Binance\n")
    else:
        print("  ✓ .env ya existe\n")
    
    # Instalar dependencias
    print_step(3, "Instalar dependencias Python")
    if run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                  "Instalar dependencias"):
        print()
    else:
        print("  ⚠️  Algunos paquetes pueden haber fallado\n")
    
    # Verificar instalación
    print_step(4, "Verificar librerías principales")
    required_packages = {
        'freqtrade': 'Freqtrade',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'tensorflow': 'TensorFlow (opcional)',
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name}")
            missing.append(package)
    
    if missing and 'tensorflow' not in missing:
        print(f"\n  ✗ Faltan dependencias: {', '.join(missing)}")
        print("  Ejecuta: pip install " + " ".join(missing))
        sys.exit(1)
    
    print()
    
    # Crear directorios
    print_step(5, "Verificar estructura de carpetas")
    dirs = ['data', 'models', 'logs', 'config']
    for d in dirs:
        path = Path(d)
        if path.exists():
            print(f"  ✓ {d}/")
        else:
            path.mkdir(exist_ok=True)
            print(f"  ✓ {d}/ (creado)")
    
    print()
    
    # Verificar archivos clave
    print_step(6, "Verificar archivos clave")
    files = [
        ('strategies/MyMlStrategy.py', 'Estrategia'),
        ('utils/ml_model.py', 'Módulo ML'),
        ('config/config.json', 'Configuración'),
        ('requirements.txt', 'Dependencias'),
    ]
    
    for file, desc in files:
        if Path(file).exists():
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc} (no encontrado)")
    
    print()
    
    # Instrucciones finales
    print_header("✅ INSTALACIÓN COMPLETADA")
    
    print("""  Próximos pasos:
  
  1️⃣  Editar credenciales:
      Abre .env y agrega:
      - BINANCE_API_KEY=tu_clave
      - BINANCE_API_SECRET=tu_secret
  
  2️⃣  Descargar datos históricos:
      python scripts/download_data.py
  
  3️⃣  Entrenar modelo de ML:
      python scripts/train_model.py
  
  4️⃣  Hacer backtesting:
      freqtrade backtesting --strategy MyMlStrategy
  
  5️⃣  Papel trading (sin dinero real):
      python scripts/run_paper_trading.py
  
  📖 Para más información:
     - README.md: Documentación completa
     - QUICKSTART.md: Guía rápida
     - notebooks/analysis.ipynb: Análisis interactivo

  ⚠️  IMPORTANTE:
     - NUNCA compartas tu BINANCE_API_SECRET
     - Comienza siempre con paper trading
     - El trading real conlleva riesgo de pérdida total

  🚀 Happy Trading!
    """)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Instalación cancelada")
        sys.exit(1)
