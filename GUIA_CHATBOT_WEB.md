# 🤖 GUÍA DE USO - CHATBOT GEMINI DE TRADING

## ¿QUÉ ES?

El Chatbot Gemini es una interfaz web interactiva que te permite hacer preguntas en tiempo real sobre Bitcoin y recibir análisis y recomendaciones de trading basadas en IA.

### Características:
- ✅ Chat interactivo con Gemini AI
- ✅ Datos en tiempo real de Bitcoin
- ✅ Predicciones horarias de máximos y mínimos
- ✅ Análisis técnico automático
- ✅ Historial de conversaciones
- ✅ Interfaz web moderna y responsive

---

## INSTALACIÓN

### Paso 1: Abrir Terminal (PowerShell)

```powershell
cd C:\github\Trading IA Bot
```

### Paso 2: Activar el Ambiente Virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Deberías ver `(.venv)` al inicio del prompt.

### Paso 3: Verificar Instalación de Dependencias

```powershell
pip list | findstr "flask"
```

Si Flask no está instalado, hazlo ahora:

```powershell
pip install flask flask-cors
```

---

## INICIAR EL SERVIDOR

### Opción 1: Desde PowerShell (RECOMENDADO)

```powershell
# 1. Activar venv
.\.venv\Scripts\Activate.ps1

# 2. Iniciar servidor
python gemini_web_server.py
```

**Salida esperada:**
```
======================================================================
🚀 SERVIDOR WEB - TRADING IA BOT CHATBOT
======================================================================

Servidor corriendo en: http://127.0.0.1:5000
Frontend: http://127.0.0.1:5000

Endpoints disponibles:
  - POST /api/chat - Enviar mensaje al chatbot
  - GET /api/bitcoin/price - Obtener precio de Bitcoin
  - GET /api/bitcoin/prediction - Predicción de máximos/mínimos
  - GET /api/conversation/<session_id> - Ver historial

======================================================================
```

### Opción 2: Doble clic en start_web_server.bat

Simplemente haz doble clic en `start_web_server.bat` y se abrirá una ventana de PowerShell ejecutando el servidor automáticamente.

---

## ACCEDER AL CHATBOT

1. **Abre tu navegador** (Chrome, Edge, Firefox, etc.)
2. **Ve a:** `http://127.0.0.1:5000`
3. **¡Listo!** Verás la interfaz del chatbot

### Pantalla Principal:

```
┌─────────────────────────────────────┬─────────────────────────────────────┐
│                                     │                                     │
│    SECCIÓN DE CHAT                  │    ANÁLISIS BITCOIN (Lado Derecho)  │
│                                     │                                     │
│  - Conversación interactiva         │  - Precio actual                    │
│  - Historial de mensajes            │  - Máximo/Mínimo 24h                │
│  - Input para nuevas preguntas      │  - Volatilidad                      │
│  - Botón para limpiar chat          │  - Predicciones por hora            │
│                                     │                                     │
└─────────────────────────────────────┴─────────────────────────────────────┘
```

---

## EJEMPLOS DE PREGUNTAS

Aquí hay preguntas que puedes hacer al chatbot:

### Sobre Precio de Bitcoin:
- ❓ "¿Cuál es el precio actual de Bitcoin?"
- ❓ "¿Cuál fue el máximo y mínimo de Bitcoin en las últimas 24 horas?"
- ❓ "¿Cuál será el precio de Bitcoin en la próxima hora?"

### Análisis Técnico:
- ❓ "¿Qué indicadores técnicos recomiendas para Bitcoin?"
- ❓ "¿Cuál es el RSI y MACD actuales de Bitcoin?"
- ❓ "¿Está en overbought o oversold el Bitcoin?"

### Recomendaciones de Trading:
- ❓ "¿Debería comprar Bitcoin ahora?"
- ❓ "¿Cuál es tu análisis para entrar en largo?"
- ❓ "¿Dónde pongo el stop loss?"

### Predicciones:
- ❓ "Predice el máximo y mínimo para la próxima hora"
- ❓ "¿Cuál será la volatilidad esperada?"
- ❓ "¿Cuáles son los niveles de soporte y resistencia?"

---

## API REST ENDPOINTS

Si prefieres usar los endpoints directamente (con curl o Postman):

### 1. Enviar Mensaje al Chatbot

```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"¿Cuál es el precio de Bitcoin?\", \"session_id\": \"user1\"}"
```

**Respuesta:**
```json
{
  "response": "El precio actual de Bitcoin es $43,245.67...",
  "bitcoin_data": {
    "current_price": 43245.67,
    "highest_24h": 44500.00,
    "lowest_24h": 42100.00,
    ...
  },
  "session_id": "user1",
  "timestamp": "2024-01-15T14:30:45.123456"
}
```

### 2. Obtener Precio Actual

```bash
curl http://127.0.0.1:5000/api/bitcoin/price
```

**Respuesta:**
```json
{
  "current_price": 43245.67,
  "highest_24h": 44500.00,
  "lowest_24h": 42100.00,
  "average_24h": 43250.00,
  "volatility": 2.5,
  "timestamp": "2024-01-15T14:30:45.123456"
}
```

### 3. Predicción de Precios

```bash
curl "http://127.0.0.1:5000/api/bitcoin/prediction?hours=1"
```

**Respuesta:**
```json
{
  "current_price": 43245.67,
  "predictions": [
    {
      "hour": 1,
      "predicted_high": 44100.18,
      "predicted_low": 42400.15,
      "confidence": 78
    }
  ],
  "volatility": 2.5,
  "timestamp": "2024-01-15T14:30:45.123456"
}
```

### 4. Ver Historial de Conversación

```bash
curl http://127.0.0.1:5000/api/conversation/user1
```

### 5. Limpiar Conversación

```bash
curl -X POST http://127.0.0.1:5000/api/clear/user1
```

---

## CARACTERÍSTICAS DE LA INTERFAZ

### Panel Izquierdo (Chat):
- **Zona de Mensajes**: Muestra toda la conversación
- **Input de Texto**: Escribe tus preguntas aquí
- **Botón Enviar**: Envía el mensaje (o presiona Enter)
- **Botón Limpiar**: Borra el historial de chat

### Panel Derecho (Análisis):
- **Datos de Bitcoin**:
  - Precio actual
  - Máximo y mínimo del día
  - Promedio del día
  - Volatilidad

- **Predicciones**:
  - Máximo predicho para la próxima hora
  - Mínimo predicho para la próxima hora
  - Nivel de confianza de la predicción

### Indicador de Estado:
- Verde (pulsante) = Servidor en línea y conectado
- Se actualiza después de cada mensaje

---

## SOLUCIÓN DE PROBLEMAS

### ❌ Error: "No se puede conectar a http://127.0.0.1:5000"

**Solución:**
1. Verifica que el servidor esté corriendo (deberías ver el mensaje "Servidor corriendo en...")
2. Espera 5 segundos después de iniciar
3. Recarga la página (Ctrl + R o Cmd + R)

### ❌ Error: "API Key inválida"

**Solución:**
1. Verifica que la API Key de Gemini esté correcta en `gemini_web_server.py`
2. Asegúrate de tener conexión a internet
3. Comprueba que tu cuenta de Google Cloud tiene la API habilitada

### ❌ El chat no responde

**Solución:**
1. Abre la consola del navegador (F12)
2. Revisa si hay errores en rojo
3. Asegúrate de que Flask está activo (mira la terminal)
4. Recarga la página

### ❌ Flask no se inicia

**Solución:**
```powershell
# Verifica Python
python --version

# Verifica pip
pip list

# Reinstala Flask
pip install --upgrade flask flask-cors
```

---

## CARACTERÍSTICAS AVANZADAS

### Múltiples Sesiones

Cada usuario puede tener su propia sesión con historial independiente:

```bash
# Usuario 1
curl -X POST http://127.0.0.1:5000/api/chat \
  -d "{\"message\": \"Hola\", \"session_id\": \"usuario1\"}"

# Usuario 2
curl -X POST http://127.0.0.1:5000/api/chat \
  -d "{\"message\": \"Hola\", \"session_id\": \"usuario2\"}"
```

### Contexto de Bitcoin en Tiempo Real

El chatbot siempre incluye:
- Precio actual de Bitcoin
- Máximos y mínimos del día
- Volatilidad calculada
- Timestamp de actualización

Esto asegura que las recomendaciones siempre estén basadas en datos actuales.

---

## INTEGRACIÓN CON FREQTRADE

El chatbot puede complementar tu estrategia de trading:

1. **Análisis Previo**: Usa el chatbot para analizar condiciones
2. **Paper Trading**: Ejecuta trades en modo papier basándose en recomendaciones
3. **Backtesting**: Revisa resultados históricos
4. **Ajustes**: Modifica parámetros basándote en insights del chatbot

---

## ESTADÍSTICAS Y MONITOREO

El servidor mantiene registro de:
- Todas las conversaciones (por sesión)
- Datos de Bitcoin generados
- Predicciones realizadas
- Timestamps de cada interacción

Puedes revisar el historial con:
```bash
curl http://127.0.0.1:5000/api/conversation/session_1234567890
```

---

## DETENER EL SERVIDOR

### Desde PowerShell:
Presiona `Ctrl + C` en la ventana del terminal

### Respuesta esperada:
```
^C
KeyboardInterrupt
Abortando servidor Flask...
```

---

## PRÓXIMAS MEJORAS

- 🔄 Integración con datos reales de Binance
- 📊 Gráficos de precios en tiempo real
- 🔔 Alertas automáticas de precios
- 💾 Base de datos para historial persistente
- 🌐 Despliegue en la nube (Heroku, Railway)

---

## RESUMEN RÁPIDO

```powershell
# 1. Activar venv
.\.venv\Scripts\Activate.ps1

# 2. Iniciar servidor
python gemini_web_server.py

# 3. Abrir navegador
# http://127.0.0.1:5000

# 4. ¡Hacer preguntas!
# "¿Cuál es el precio de Bitcoin?"
```

---

## SOPORTE

Si tienes problemas:
1. Verifica la terminal del servidor para mensajes de error
2. Abre la consola del navegador (F12) para ver errores de frontend
3. Asegúrate de que todos los paquetes están instalados: `pip list`
4. Reinicia el servidor completamente

¡Disfruta del chatbot! 🚀
