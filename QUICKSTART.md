# Guía Rápida - Trading IA Bot

## 🚀 Inicio Rápido (5 minutos)

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales
```bash
cp .env.example .env
# Editar .env con tus claves de Binance
```

### 3. Ejecutar primera vez
```bash
# Descargar datos
python scripts/download_data.py

# Entrenar modelo
python scripts/train_model.py

# Hacer backtest
freqtrade backtesting --strategy MyMlStrategy --timeframe 1h

# Paper trading (sin dinero real)
python scripts/run_paper_trading.py
```

---

## 📊 Componentes Principales

### `strategies/MyMlStrategy.py`
- **Qué hace**: Define lógica de compra/venta
- **Key methods**:
  - `populate_indicators()`: Calcula indicadores
  - `populate_entry_trend()`: Señales de compra
  - `populate_exit_trend()`: Señales de venta

### `utils/ml_model.py`
- **MLModel**: Entrena y predice con Random Forest/Gradient Boosting
- **FeatureEngineer**: Calcula indicadores técnicos
  - RSI, MACD, Bollinger Bands, ATR, volatilidad

### `config/config.json`
- Configuración de exchange, pares, stake, etc.
- Parámetros de backtesting e hyperopt

### `scripts/`
- `download_data.py`: Descargar OHLCV histórico
- `train_model.py`: Entrenar modelos de ML
- `run_paper_trading.py`: Ejecutar en modo prueba

---

## 🧠 Cómo Funciona

```
1. Descarga datos históricos OHLCV
                    ↓
2. Calcula indicadores técnicos (RSI, MACD, etc.)
                    ↓
3. Entrena modelo ML con scikit-learn
                    ↓
4. Genera señales de compra/venta basadas en:
   - Indicadores técnicos (40%)
   - Predicciones de ML (60%)
                    ↓
5. Simula trades en datos históricos (backtesting)
                    ↓
6. Optimiza parámetros automáticamente
                    ↓
7. Ejecuta en vivo (paper o real trading)
```

---

## ⚙️ Parámetros Ajustables

En `MyMlStrategy`:

```python
# RSI Thresholds
buy_rsi = 30          # Comprar cuando RSI < 30
sell_rsi = 70         # Vender cuando RSI > 70

# ML Confidence
ml_buy_threshold = 0.65   # Necesita 65%+ confianza para comprar
ml_sell_threshold = 0.35  # Vende si confianza < 35%

# Pesos
ml_weight = 0.6       # 60% ML, 40% indicadores técnicos

# Risk Management
stoploss = -0.05      # Máx. pérdida -5%
minimal_roi = {"0": 0.10}  # Objetivo ganancia 10%
```

---

## 📈 Métricas Clave

| Métrica | Bueno | Excelente |
|---------|-------|-----------|
| Win Rate | > 50% | > 60% |
| Sharpe Ratio | > 1.0 | > 2.0 |
| Profit Factor | > 1.5 | > 2.5 |
| Max Drawdown | < 20% | < 10% |
| Calmar Ratio | > 2.0 | > 5.0 |

---

## 🔄 Flujo de Trabajo

### Desarrollo
```bash
# 1. Editar estrategia
vim strategies/MyMlStrategy.py

# 2. Entrenar modelo
python scripts/train_model.py

# 3. Hacer backtest
freqtrade backtesting --strategy MyMlStrategy

# 4. Optimizar parámetros
freqtrade hyperopt --strategy MyMlStrategy --epochs 100
```

### Testing
```bash
# Paper trading (recomendado 2-4 semanas)
python scripts/run_paper_trading.py

# Ver logs
tail -f logs/freqtrade.log

# Dashboard
http://localhost:8080
```

### Producción
```bash
# SOLO después de testing exitoso:
# 1. Cambiar config.json: "dry_run": false
# 2. Verificar stake_amount (comenzar pequeño)
# 3. Ejecutar
freqtrade trade --strategy MyMlStrategy
```

---

## ⚠️ Riesgos y Mejores Prácticas

### ✅ QUÉ HACER
- ✓ Comenzar siempre en paper trading
- ✓ Usar montos pequeños en trading real
- ✓ Monitorear diariamente
- ✓ Mantener stoploss agresivo
- ✓ Reentrenar modelo cada 4 semanas
- ✓ Hacer backup de modelos entrenados

### ❌ QUÉ EVITAR
- ✗ Trading real sin paper trading previo
- ✗ Invertir todo el capital en un trade
- ✗ Ignorar warns del bot
- ✗ Cambiar parámetros sin backtesting
- ✗ Dejar corriendo sin monitoreo
- ✗ Suponer que resultados pasados = futuros

---

## 🐛 Troubleshooting

### Error: "Modelo no entrenado"
```bash
python scripts/train_model.py
```

### Error: "No data found"
```bash
python scripts/download_data.py --days 90
```

### Backtesting muy lento
```bash
# Usar menos datos
freqtrade backtesting --timerange 20231101-20231201
```

### Memoria insuficiente
```bash
# Limitar número de procesos
export OPENBLAS_NUM_THREADS=1
freqtrade backtesting ...
```

---

## 📚 Recursos

- [Freqtrade Docs](https://www.freqtrade.io/en/stable/)
- [Scikit-learn Docs](https://scikit-learn.org/)
- [Binance API](https://binance-docs.github.io/apidocs/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

## 📞 Soporte

Para problemas:
1. Revisar logs: `logs/freqtrade.log`
2. Consultar documentación oficial
3. Verificar configuración en `config/config.json`
4. Probar en paper trading antes de trading real

---

**Última actualización**: Noviembre 12, 2025

*⚠️ Disclaimer: Este bot es para fines educativos. El trading de criptomonedas es arriesgado. Usa bajo tu propio riesgo.*
