#!/usr/bin/env python3
"""
Script para entrenar el modelo de ML con datos históricos.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ml_model import MLModel, FeatureEngineer


def load_historical_data(data_path: str, pair: str, timeframe: str = '1h') -> pd.DataFrame:
    """
    Carga datos históricos desde archivos JSON.
    
    Args:
        data_path: Ruta del directorio de datos
        pair: Pareja (ej. BTC/USDT)
        timeframe: Timeframe (ej. 1h)
        
    Returns:
        DataFrame con datos OHLCV
    """
    
    # Convertir formato de pareja para archivo
    pair_str = pair.replace('/', '_')
    file_path = Path(data_path) / 'binance' / f'{pair_str}-{timeframe}.json'
    
    if not file_path.exists():
        print(f"✗ Archivo no encontrado: {file_path}")
        return None
    
    print(f"📂 Cargando datos desde: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df = df.set_index('date')
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df = df.astype(float)
    
    print(f"✓ Datos cargados: {len(df)} velas")
    print(f"  Período: {df.index[0]} a {df.index[-1]}")
    
    return df


def train_model_on_data(df: pd.DataFrame, model_type: str = 'random_forest') -> dict:
    """
    Entrena un modelo de ML con los datos históricos.
    
    Args:
        df: DataFrame con datos OHLCV
        model_type: Tipo de modelo ('random_forest' o 'gradient_boosting')
        
    Returns:
        Diccionario con métricas del entrenamiento
    """
    
    print(f"\n🧠 Iniciando entrenamiento del modelo ({model_type})...")
    
    # Inicializar modelo y feature engineer
    model = MLModel(model_type=model_type)
    feature_engineer = FeatureEngineer()
    
    # Agregar indicadores técnicos
    print("📊 Calculando indicadores técnicos...")
    df = feature_engineer.add_technical_indicators(df)
    
    # Definir features
    feature_cols = [
        'rsi_14', 'macd', 'macd_signal', 'macd_diff',
        'bb_upper', 'bb_middle', 'bb_lower', 'atr', 'volatility',
        'price_change_1h', 'price_change_4h', 'volume_change'
    ]
    
    # Entrenar modelo
    print(f"🎓 Entrenando modelo con {len(df)} muestras...")
    metrics = model.train(df, feature_cols, threshold=0.01, test_size=0.2)
    
    # Mostrar resultados
    print("\n✓ Entrenamiento completado!")
    print(f"  Exactitud:  {metrics['accuracy']:.4f}")
    print(f"  Precisión: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1-Score:  {metrics['f1']:.4f}")
    print(f"  Muestras de entrenamiento: {metrics['train_size']}")
    print(f"  Muestras de prueba:        {metrics['test_size']}")
    
    return model, metrics


def main():
    """Función principal."""
    
    # Rutas
    DATA_PATH = 'data/'
    MODELS_PATH = 'models/'
    
    # Crear directorio de modelos si no existe
    Path(MODELS_PATH).mkdir(exist_ok=True)
    
    # Configuración
    PAIRS = ['BTC/USDT', 'ETH/USDT']
    TIMEFRAME = '1h'
    
    print("=" * 60)
    print("ENTRENAMIENTO DE MODELO DE ML PARA TRADING")
    print("=" * 60)
    
    models_trained = []
    
    for pair in PAIRS:
        print(f"\n{'='*60}")
        print(f"Procesando pareja: {pair}")
        print(f"{'='*60}")
        
        # Cargar datos
        df = load_historical_data(DATA_PATH, pair, TIMEFRAME)
        
        if df is None or len(df) < 100:
            print(f"⚠ Datos insuficientes para {pair}")
            continue
        
        # Entrenar modelo
        model, metrics = train_model_on_data(df, model_type='random_forest')
        
        # Guardar modelo
        model_file = model.save_model(f"{pair.replace('/', '_')}_{TIMEFRAME}")
        print(f"\n💾 Modelo guardado: {model_file}")
        
        models_trained.append({
            'pair': pair,
            'timeframe': TIMEFRAME,
            'model_file': model_file,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        })
    
    # Crear un modelo combinado (opcional)
    if len(models_trained) > 0:
        print(f"\n{'='*60}")
        print("Resumen de Entrenamiento")
        print(f"{'='*60}")
        print(f"✓ Modelos entrenados: {len(models_trained)}")
        
        for item in models_trained:
            print(f"\n  {item['pair']} ({item['timeframe']})")
            print(f"    F1-Score: {item['metrics']['f1']:.4f}")
            print(f"    Archivo: {item['model_file']}")
        
        # Guardar información de entrenamiento
        summary_file = Path(MODELS_PATH) / 'training_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(models_trained, f, indent=2)
        
        print(f"\n📋 Resumen guardado en: {summary_file}")


if __name__ == '__main__':
    main()
