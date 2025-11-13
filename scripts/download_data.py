#!/usr/bin/env python3
"""
Script para descargar datos históricos para backtesting.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta


def download_data(pairs: list, timeframes: list, days: int = 30):
    """
    Descarga datos históricos usando Freqtrade.
    
    Args:
        pairs: Lista de parejas (ej. ['BTC/USDT', 'ETH/USDT'])
        timeframes: Lista de timeframes (ej. ['1h', '4h'])
        days: Días hacia atrás a descargar
    """
    
    print(f"📥 Descargando datos para {len(pairs)} parejas...")
    print(f"   Parejas: {', '.join(pairs)}")
    print(f"   Timeframes: {', '.join(timeframes)}")
    print(f"   Período: Últimos {days} días\n")
    
    for timeframe in timeframes:
        print(f"⏱️  Descargando datos de {timeframe}...")
        
        pairs_str = ' '.join(pairs)
        
        cmd = [
            'freqtrade', 'download-data',
            f'--pairs {pairs_str}',
            f'--timeframe {timeframe}',
            f'--days {days}',
            '--exchange binance',
            '--data-format json'
        ]
        
        try:
            result = subprocess.run(' '.join(cmd), shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ {timeframe} descargado correctamente\n")
            else:
                print(f"✗ Error descargando {timeframe}")
                print(result.stderr)
        
        except Exception as e:
            print(f"✗ Error: {e}")


def list_available_pairs():
    """Lista parejas disponibles para descargar."""
    
    common_pairs = [
        'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT',
        'XRP/USDT', 'DOGE/USDT', 'AVAX/USDT', 'MATIC/USDT', 'LINK/USDT',
        'LUNC/USDT', 'ICP/USDT', 'NEAR/USDT', 'ARB/USDT', 'OP/USDT'
    ]
    
    return common_pairs


if __name__ == '__main__':
    
    # Configuración
    PAIRS = [
        'BTC/USDT',
        'ETH/USDT',
        'BNB/USDT',
    ]
    
    TIMEFRAMES = ['1h', '4h']
    DAYS = 90
    
    # Ejecutar descarga
    download_data(PAIRS, TIMEFRAMES, DAYS)
    
    print("\n✅ Descarga completada!")
    print(f"   Los datos se guardaron en: user_data/data/binance/")
