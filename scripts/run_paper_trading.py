"""
Script para ejecutar la estrategia en modo paper trading (prueba sin dinero real).
"""

import subprocess
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


def main():
    """Inicia el bot en modo paper trading."""
    
    # Cargar variables de entorno
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        load_dotenv(env_file)
    else:
        print("⚠️ Archivo .env no encontrado. Usando valores por defecto.")
        print("   Ejecuta: cp .env.example .env")
    
    print("=" * 60)
    print("🤖 TRADING IA BOT - MODO PAPER TRADING")
    print("=" * 60)
    print()
    print("⚠️  Modo DRY-RUN: No se usará dinero real")
    print("✓ Se usará balance simulado de $1000")
    print()
    
    # Comando para iniciar el bot
    cmd = [
        'freqtrade', 'trade',
        '--strategy', 'MyMlStrategy',
        '--dry-run',  # Modo papel
        '--db-url', 'sqlite:///tradesv3.sqlite',
        '--logfile', 'logs/freqtrade.log'
    ]
    
    try:
        print("🚀 Iniciando bot...")
        subprocess.run(' '.join(cmd), shell=True)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Bot detenido por el usuario")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
