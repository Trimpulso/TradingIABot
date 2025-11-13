"""
Módulo de utilidades para análisis y visualización.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json


def load_trade_results(results_file: str) -> pd.DataFrame:
    """
    Carga resultados de backtesting.
    
    Args:
        results_file: Ruta del archivo backtest-result.json
        
    Returns:
        DataFrame con resultados de trades
    """
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    trades_df = pd.DataFrame(data['trades'])
    return trades_df


def calculate_metrics(trades_df: pd.DataFrame) -> dict:
    """
    Calcula métricas de rendimiento.
    
    Args:
        trades_df: DataFrame con trades
        
    Returns:
        Diccionario con métricas
    """
    
    metrics = {
        'total_trades': len(trades_df),
        'winning_trades': len(trades_df[trades_df['profit_abs'] > 0]),
        'losing_trades': len(trades_df[trades_df['profit_abs'] < 0]),
        'win_rate': len(trades_df[trades_df['profit_abs'] > 0]) / len(trades_df) * 100,
        'total_profit': trades_df['profit_abs'].sum(),
        'avg_profit_per_trade': trades_df['profit_percent'].mean(),
        'max_profit': trades_df['profit_percent'].max(),
        'max_loss': trades_df['profit_percent'].min(),
        'sharpe_ratio': trades_df['profit_percent'].mean() / trades_df['profit_percent'].std() if trades_df['profit_percent'].std() > 0 else 0,
    }
    
    return metrics


def plot_equity_curve(trades_df: pd.DataFrame, initial_balance: float = 1000):
    """
    Grafica la curva de capital acumulado.
    
    Args:
        trades_df: DataFrame con trades
        initial_balance: Balance inicial
    """
    
    trades_df_sorted = trades_df.sort_values('close_date')
    equity = initial_balance + trades_df_sorted['profit_abs'].cumsum()
    
    plt.figure(figsize=(12, 6))
    plt.plot(equity, linewidth=2, label='Equity')
    plt.xlabel('Trade #')
    plt.ylabel('Capital ($)')
    plt.title('Curva de Capital')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_returns_distribution(trades_df: pd.DataFrame):
    """
    Grafica la distribución de retornos.
    
    Args:
        trades_df: DataFrame con trades
    """
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histograma
    axes[0].hist(trades_df['profit_percent'] * 100, bins=20, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Retorno (%)')
    axes[0].set_ylabel('Frecuencia')
    axes[0].set_title('Distribución de Retornos')
    axes[0].axvline(trades_df['profit_percent'].mean() * 100, color='red', linestyle='--', label='Media')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Box plot por resultado
    data_to_plot = [
        trades_df[trades_df['profit_abs'] > 0]['profit_percent'] * 100,
        trades_df[trades_df['profit_abs'] < 0]['profit_percent'] * 100
    ]
    
    axes[1].boxplot(data_to_plot, labels=['Ganancias', 'Pérdidas'])
    axes[1].set_ylabel('Retorno (%)')
    axes[1].set_title('Distribución de Ganancias vs Pérdidas')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    
    # Ejemplo de uso
    results_file = 'backtest-result.json'
    
    if Path(results_file).exists():
        df = load_trade_results(results_file)
        metrics = calculate_metrics(df)
        
        print("=" * 50)
        print("MÉTRICAS DE RENDIMIENTO")
        print("=" * 50)
        for key, value in metrics.items():
            print(f"{key}: {value}")
        
        # Gráficos
        plot_equity_curve(df)
        plot_returns_distribution(df)
