# 🚀 CÓMO VER Y EJECUTAR EL PROYECTO

## 📍 OPCIÓN 1: VER EN GITHUB (Lo más rápido)

### Desde cualquier navegador:

1. **Ve a:**
   ```
   https://github.com/Trimpulso/TradingIABot
   ```

2. **Verás:**
   - 📋 README.md con descripción completa
   - 📁 Estructura de carpetas
   - 📊 Todos los archivos organizados
   - 📈 Commits y historial

3. **Para ver código específico:**
   - Click en `strategies/MyMlStrategy.py` para ver la estrategia
   - Click en `utils/ml_model.py` para ver los modelos
   - Click en `notebooks/analysis.ipynb` para ver el notebook

---

## 💻 OPCIÓN 2: CLONAR Y EJECUTAR LOCALMENTE

### Paso 1: Clonar el repositorio

```bash
# Abrir PowerShell y ejecutar:
git clone https://github.com/Trimpulso/TradingIABot.git
cd TradingIABot
```

### Paso 2: Instalar dependencias

```bash
# Automático (recomendado):
python install.py

# O manual:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 3: Configurar credenciales

```bash
# Copiar template:
copy .env.example .env

# Editar .env con tus claves Binance:
BINANCE_API_KEY=tu_clave
BINANCE_API_SECRET=tu_secret
```

### Paso 4: Ejecutar scripts

```bash
# Descargar datos históricos:
python scripts/download_data.py

# Entrenar modelo:
python scripts/train_model.py

# Ver análisis interactivo:
jupyter notebook notebooks/analysis.ipynb

# Hacer backtest:
freqtrade backtesting --strategy MyMlStrategy

# Paper trading (sin dinero real):
python scripts/run_paper_trading.py
```

---

## 📓 OPCIÓN 3: VER EL NOTEBOOK INTERACTIVO

### En GitHub (online, sin instalar nada):

1. Ve a: https://github.com/Trimpulso/TradingIABot
2. Entra en: `notebooks/analysis.ipynb`
3. GitHub lo renderiza automáticamente
4. Verás:
   - 📊 Gráficos de datos
   - 📈 Análisis de modelos
   - 🔬 Feature engineering
   - 📉 Backtesting

### Localmente (interactivo):

```bash
# Clonar repo
git clone https://github.com/Trimpulso/TradingIABot.git
cd TradingIABot

# Instalar Jupyter
pip install jupyter

# Abrir notebook
jupyter notebook notebooks/analysis.ipynb
```

---

## 📖 OPCIÓN 4: LEER LA DOCUMENTACIÓN

### En GitHub:

1. **README.md** - Documentación técnica completa
2. **QUICKSTART.md** - Guía rápida (5 minutos)
3. **DELIVERABLES.md** - Resumen ejecutivo

### Localmente:

```bash
# Simplemente abre los archivos .md con cualquier editor
# O en VS Code:
code README.md
```

---

## 🎮 OPCIÓN 5: EJECUTAR EN VS CODE

### Paso 1: Abrir proyecto

```bash
# Opción A: Desde PowerShell
cd "c:\github\Trading IA Bot"
code .

# Opción B: Directamente en VS Code
# File → Open Folder → Seleccionar "Trading IA Bot"
```

### Paso 2: Ejecutar scripts desde VS Code

1. **Abrir terminal integrada:**
   - Ctrl + ` (backtick)
   - O: View → Terminal

2. **Ejecutar script:**
   ```bash
   python scripts/download_data.py
   python scripts/train_model.py
   ```

3. **Ver archivos Python:**
   - Click izquierdo en `strategies/MyMlStrategy.py`
   - Verás código coloreado y con autocompletado

---

## 🔍 OPCIÓN 6: EXPLORAR CARPETAS

### Estructura visible en GitHub:

```
📁 TradingIABot/
  ├── 📄 README.md ← Lee esto primero
  ├── 📄 QUICKSTART.md ← Guía rápida
  │
  ├── 🤖 strategies/
  │   └── MyMlStrategy.py (click para ver código)
  │
  ├── 🧠 utils/
  │   ├── ml_model.py (click para ver código)
  │   └── analysis.py (click para ver código)
  │
  ├── 🛠️ scripts/
  │   ├── download_data.py
  │   ├── train_model.py
  │   └── run_paper_trading.py
  │
  └── 📊 notebooks/
      └── analysis.ipynb (abre interactivo)
```

---

## ⚡ FLUJO RECOMENDADO

### Para aprender (10 minutos):

1. Ve a GitHub: https://github.com/Trimpulso/TradingIABot
2. Lee `README.md` (en GitHub, no necesitas clonar)
3. Abre `notebooks/analysis.ipynb` (GitHub lo renderiza)
4. Entiende la estructura leyendo `QUICKSTART.md`

### Para experimentar (1 hora):

```bash
# 1. Clonar
git clone https://github.com/Trimpulso/TradingIABot.git
cd TradingIABot

# 2. Instalar
python install.py

# 3. Explorar en VS Code
code .

# 4. Ejecutar notebook
jupyter notebook notebooks/analysis.ipynb
```

### Para trading (1-2 semanas):

```bash
# 1. Configurar .env con claves Binance
edit .env

# 2. Descargar datos
python scripts/download_data.py

# 3. Entrenar modelo
python scripts/train_model.py

# 4. Hacer backtest
freqtrade backtesting --strategy MyMlStrategy

# 5. Paper trading (sin dinero real)
python scripts/run_paper_trading.py

# 6. Si todo va bien, trading real (con pequeños montos)
# Cambiar config.json: "dry_run": false
freqtrade trade --strategy MyMlStrategy
```

---

## 🎯 COMANDOS RÁPIDOS

### Para correr desde cualquier lado:

```bash
# Ir al proyecto
cd "c:\github\Trading IA Bot"

# Ver archivos
ls -la

# Ejecutar Jupyter
jupyter notebook

# Ejecutar script
python scripts/train_model.py

# Ver status de Git
git status
git log

# Hacer cambios y subir
git add .
git commit -m "Mi cambio"
git push origin master
```

---

## 📋 CHECKLIST: ¿QUÉ NECESITO?

Para ver en GitHub (¡GRATIS!):
- ✓ Navegador web
- ✓ 5 minutos
- ✓ Nada más

Para ejecutar localmente:
- ✓ Python 3.8+
- ✓ Git
- ✓ ~2 GB de espacio disco
- ✓ 30 minutos instalación
- ✓ Credenciales Binance (si quieres trading real)

---

## ✅ AHORA ¿QUÉ?

Elige una opción:

**Opción A (5 min):** Solo mirar código
→ Ve a https://github.com/Trimpulso/TradingIABot

**Opción B (1 hora):** Aprender cómo funciona
→ Clona y ejecuta `jupyter notebook`

**Opción C (1-2 semanas):** Usar para trading real
→ Sigue los pasos de instalación y paper trading

---

## 🚀 COMIENZA AHORA

**La forma más rápida es:**

1. Abre en navegador:
   https://github.com/Trimpulso/TradingIABot

2. Lee `README.md`

3. Haz click en `notebooks/analysis.ipynb`

**¡Eso es todo para comenzar!** 📊

---

Cualquier pregunta sobre los pasos, ¡solo pregunta!
