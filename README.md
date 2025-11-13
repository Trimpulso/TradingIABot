# 🤖 Trading IA Bot - Machine Learning + Freqtrade

Un bot de trading automático impulsado por Machine Learning, construido con **Freqtrade** para el trading de criptomonedas con lógica inteligente de compra/venta.

## 📋 Características

✅ **Estrategia basada en ML**: Combina predicciones de modelos de ML con indicadores técnicos tradicionales  
✅ **Backtesting robusto**: Prueba estrategias con datos históricos  
✅ **Optimización Hyperopt**: Ajusta automáticamente parámetros para maximizar rendimiento  
✅ **Trading en vivo**: Integración directa con exchanges (Binance, Kraken, etc.)  
✅ **Feature Engineering**: Ingeniería de características automática  
✅ **Modelos múltiples**: Soporte para Random Forest, Gradient Boosting y redes LSTM  

---

## 🏗️ Arquitectura

```
Trading IA Bot/
├── strategies/              # Archivos de estrategia
│   └── MyMlStrategy.py      # Estrategia principal con ML
├── models/                  # Modelos entrenados
│   ├── random_forest_latest.pkl
│   └── training_summary.json
├── data/                    # Datos históricos (OHLCV)
│   └── binance/
├── config/                  # Configuración
│   └── config.json
├── utils/                   # Módulos reutilizables
│   ├── ml_model.py          # Clase MLModel y FeatureEngineer
│   └── feature_engineer.py
├── scripts/                 # Scripts de utilidad
│   ├── download_data.py     # Descargar datos históricos
│   ├── train_model.py       # Entrenar modelos de ML
│   └── backtest.sh          # Ejecutar backtesting
├── notebooks/               # Análisis exploratorio
│   └── analysis.ipynb
└── requirements.txt         # Dependencias Python
```

---

## 🚀 Configuración Inicial

### 1. Instalar Dependencias

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Credenciales

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# BINANCE_API_KEY=your_key
# BINANCE_API_SECRET=your_secret
```

### 3. Descargar Datos Históricos

```bash
python scripts/download_data.py
```

### 4. Entrenar Modelo de ML

```bash
python scripts/train_model.py
```

---

## 📊 Flujo de Trabajo

### 🔄 Backtesting

```bash
freqtrade backtesting \
    --strategy MyMlStrategy \
    --timeframe 1h \
    --max-open-trades 3 \
    --timerange 20230101-20231231
```

### 🎯 Optimización de Hiperparámetros

```bash
freqtrade hyperopt \
    --strategy MyMlStrategy \
    --hyperopt-loss SharpeHyperOptLoss \
    --epochs 100 \
    --timerange 20230101-20231231
```

### 🏃 Trading en Vivo (Paper Trading)

```bash
freqtrade trade \
    --strategy MyMlStrategy \
    --dry-run  # Remover para trading real
```

---

## 🧠 Componentes de ML

### Feature Engineering (`utils/ml_model.py`)

La clase `FeatureEngineer` calcula automáticamente:

- **RSI** (14, 21): Índice de Fuerza Relativa
- **MACD**: Convergencia/Divergencia de Medias Móviles
- **Bollinger Bands**: Bandas de Bollinger (σ=2)
- **ATR**: Rango Verdadero Promedio
- **Volatilidad**: Desviación estándar de 20 velas
- **Cambios de Precio**: 1h y 4h
- **Volumen**: Cambio de volumen

### Modelos Disponibles

#### Random Forest
```python
MLModel(model_type='random_forest')
# 100 árboles, max_depth=15, optimizado para clasificación
```

#### Gradient Boosting
```python
MLModel(model_type='gradient_boosting')
# 100 estimadores, learning_rate=0.1
```

### Lógica de Decisión

La estrategia combina indicadores técnicos y predicciones de ML:

$$\text{SEÑAL COMPRA} = (1-w) \times \text{Técnica} + w \times \text{ML}$$

Donde $w = 0.6$ (peso ajustable del ML)

**Umbral de confianza**: 0.65 (65% mínimo para comprar)

---

## ⚙️ Parametrización

### Parámetros Principales (`MyMlStrategy.py`)

```python
# RSI
buy_rsi = 30          # Comprar cuando RSI < 30
sell_rsi = 70         # Vender cuando RSI > 70

# ML
ml_buy_threshold = 0.65    # Confianza mínima para comprar
ml_sell_threshold = 0.35   # Confianza máxima para vender
ml_weight = 0.6            # Peso del ML en decisión

# Risk Management
stoploss = -0.05      # -5% pérdida máxima
minimal_roi = {"0": 0.10}  # 10% ganancia objetivo
```

### Optimización Automática

Usa Hyperopt para encontrar los mejores parámetros:

```bash
freqtrade hyperopt \
    --hyperopt-loss SharpeHyperOptLoss \
    --spaces buy sell roi stoploss \
    --epochs 100
```

---

## 📈 Monitoreo en Tiempo Real

### Panel Web (API REST)

```bash
freqtrade trade --strategy MyMlStrategy
# Acceder a http://localhost:8080
```

### Notificaciones Telegram (opcional)

Configura en `config/config.json`:

```json
"telegram": {
    "enabled": true,
    "token": "YOUR_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
}
```

---

## 🔍 Debugging y Análisis

### Jupyter Notebook

```bash
jupyter notebook notebooks/analysis.ipynb
```

### Logs

```bash
# Trading en vivo
freqtrade trade --strategy MyMlStrategy --logfile logs/trade.log

# Backtesting
freqtrade backtesting --logfile logs/backtest.log
```

---

## ⚠️ Riesgos y Consideraciones

1. **Trading en Vivo**: Comienza siempre con cantidades pequeñas
2. **Overfitting**: El modelo puede sobreajustarse a datos históricos
3. **Market Conditions**: Las condiciones pasadas no garantizan resultados futuros
4. **Volatilidad**: Alta volatilidad puede causar pérdidas rápidas
5. **Fees**: Los fees del exchange impactan la rentabilidad

### Best Practices

✅ Usar `--dry-run` para pruebas  
✅ Hacer backtest frecuentemente con datos nuevos  
✅ Mantener stoploss agresivo (-5% máximo)  
✅ Limitar máximo de trades abiertos  
✅ Monitorear rendimiento regularmente  
✅ Actualizar modelo cada 4-8 semanas  

---

## 🛠️ Troubleshooting

### Modelo no entrena
```bash
# Verificar datos
python -c "
import pandas as pd
df = pd.read_json('data/binance/BTC_USDT-1h.json')
print(f'Filas: {len(df)}')
"
```

### Backtest falla
```bash
# Verificar estrategia
freqtrade strategy-list
freqtrade show-config
```

### Memoria insuficiente
```bash
# Usar menos datos
freqtrade backtesting --timerange 20230901-20231231
```

---

## 📚 Recursos Adicionales

- [Documentación Freqtrade](https://www.freqtrade.io/en/stable/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Binance API](https://binance-docs.github.io/apidocs/)
- [TensorFlow/Keras](https://www.tensorflow.org/)

---

## 📝 Licencia

MIT License - Usa libremente con propósitos educativos

---

## ⚡ Próximas Mejoras

- [ ] Integración con modelos LSTM (Keras)
- [ ] Ensemble de múltiples modelos
- [ ] Sistema de alerts avanzado
- [ ] Análisis de sentimiento (Twitter/Reddit)
- [ ] Integración con más exchanges
- [ ] Dashboard mejorado
- [ ] Caché de predicciones

---

**¡Happy Trading! 🚀**

*Recuerda: Este bot es para fines educativos. Usa con prudencia y siempre a riesgo propio.*
