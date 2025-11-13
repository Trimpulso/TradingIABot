#!/bin/bash

# Script para ejecutar backtesting con Freqtrade

echo "=========================================="
echo "BACKTESTING CON FREQTRADE"
echo "=========================================="

# Variables
STRATEGY="MyMlStrategy"
TIMEFRAME="1h"
STAKE="100"
DRY_RUN="true"

# Ejecutar backtest
echo ""
echo "🔄 Iniciando backtest..."
echo "   Estrategia: $STRATEGY"
echo "   Timeframe: $TIMEFRAME"
echo "   Stake: $STAKE USDT"
echo ""

freqtrade backtesting \
    --strategy $STRATEGY \
    --timeframe $TIMEFRAME \
    --stake-amount $STAKE \
    --dry-run \
    --max-open-trades 3 \
    --timerange 20230101-20231231

echo ""
echo "✅ Backtest completado!"
echo ""
echo "Resultados en:"
echo "  - backtest-result.json"
echo "  - backtest_plot.html"
