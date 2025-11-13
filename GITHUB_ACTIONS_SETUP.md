🤖 GITHUB ACTIONS - EJECUCIÓN AUTOMÁTICA
═════════════════════════════════════════════════════════════════

¡YA ESTÁ CONFIGURADO! Acabo de crear 3 workflows automáticos.

═════════════════════════════════════════════════════════════════

📊 WORKFLOW 1: WEEKLY BACKTEST (Cada domingo 2 AM)
═════════════════════════════════════════════════════════════════

¿QUÉ HACE?
- Entrena el modelo ML automáticamente
- Ejecuta backtest de la estrategia
- Genera reporte de resultados
- Guarda artefactos durante 30 días

¿CUÁNDO?
- Cada domingo a las 2 AM UTC (9 PM domingo EST)
- O manualmente desde GitHub UI

RESULTADO:
- Backtest completo
- Artefactos guardados en "Actions"
- Modelo actualizado


🔍 WORKFLOW 2: CODE QUALITY (Cada miércoles 3 AM)
═════════════════════════════════════════════════════════════════

¿QUÉ HACE?
- Verifica formato del código (Black)
- Análisis estático (Flake8)
- Valida configuración JSON
- Cuenta líneas de código

¿CUÁNDO?
- Cada miércoles a las 3 AM UTC
- Cada push a master/main/develop


📝 WORKFLOW 3: WEEKLY REPORT (Cada viernes 5 PM)
═════════════════════════════════════════════════════════════════

¿QUÉ HACE?
- Genera reporte JSON
- Crea markdown con status
- Guarda historial de 90 días
- Muestra próximos pasos

¿CUÁNDO?
- Cada viernes a las 5 PM UTC
- O manualmente


═════════════════════════════════════════════════════════════════

🔍 ¿CÓMO VER LOS RESULTADOS?

OPCIÓN A: En GitHub UI (sin instalar nada)
───────────────────────────────────────────

1. Ve a: https://github.com/Trimpulso/TradingIABot

2. Click en tab: "Actions" (entre "Pull requests" e "Insights")

3. Verás lista de workflows ejecutados

4. Click en cualquiera para ver:
   ✓ Logs en tiempo real
   ✓ Duración
   ✓ Status (✅ éxito o ❌ error)
   ✓ Artefactos (resultados)

5. Descarga artefactos:
   - backtest-results/
   - quality-report/
   - weekly-reports/


OPCIÓN B: Desde terminal local
───────────────────────────────

git log --all --oneline | grep -E "🤖|📊"


═════════════════════════════════════════════════════════════════

📅 CRONOGRAMA AUTOMÁTICO

Hora UTC    │ Día          │ Workflow              │ Qué hace
─────────────┼──────────────┼──────────────────────┼──────────────
02:00 UTC   │ Cada domingo │ weekly_backtest.yml  │ Backtest + ML
03:00 UTC   │ Cada miércoles│ code_quality.yml    │ Análisis código
17:00 UTC   │ Cada viernes │ weekly_report.yml    │ Reporte status


═════════════════════════════════════════════════════════════════

⚡ EJECUCIÓN MANUAL

Si quieres ejecutar ahora sin esperar:

1. Ve a: https://github.com/Trimpulso/TradingIABot/actions

2. Click en el workflow que quieras (ej: "📊 Weekly Backtest & Model Training")

3. Click botón azul: "Run workflow"

4. Click "Run workflow" de nuevo en popup

5. Se ejecuta inmediatamente ⚡


═════════════════════════════════════════════════════════════════

💾 ARTEFACTOS (Resultados guardados)

Cada workflow crea artefactos descargables:

BACKTEST:
- backtest_results/
- models/ (modelos entrenados)

QUALITY:
- quality-report/

REPORTS:
- weekly_reports/
- WEEKLY_STATUS.md

Duración:
- Backtest: 30 días
- Quality: 7 días
- Reports: 90 días


═════════════════════════════════════════════════════════════════

⚙️ PERSONALIZACIÓN

Para cambiar horarios, edita en GitHub:

.github/workflows/weekly_backtest.yml

Busca esta línea:
```
- cron: '0 2 * * 0'  # Cada domingo 2 AM
```

Formato cron:
- '0 2 * * 0' = 02:00 UTC, domingo
- '0 14 * * 5' = 14:00 UTC, viernes

Generador: https://crontab.guru/


═════════════════════════════════════════════════════════════════

🚨 LIMITACIONES

GitHub Actions GRATIS:
- 2,000 minutos/mes
- 500 MB almacenamiento
- Sin acceso a credenciales (⚠️)

Para trading real necesitarías:
- Guardar API keys en GitHub Secrets
- Cambiar a 'sell' mode (en config.json)
- Usar action automática para mandar ordenes

RECOMENDACIÓN:
- Ahora: Backtest automático (sin credenciales)
- Luego: Migrar a servidor (Heroku/Railway) para trading real


═════════════════════════════════════════════════════════════════

🎯 PRÓXIMOS PASOS

1. ✅ Verifica que los workflows se ejecutan:
   https://github.com/Trimpulso/TradingIABot/actions

2. ✅ Ejecuta manualmente el backtest (azul "Run workflow")

3. ✅ Ve los resultados en 2-3 minutos

4. ✅ Descarga artefactos (si quieres analizarlos localmente)

5. ✅ Configura notificaciones si quieres alertas


═════════════════════════════════════════════════════════════════

✨ ¿QUÉ CONSEGUISTE?

✅ Bot ejecutándose automáticamente en la nube
✅ Sin tu PC encendida
✅ Sin instalar nada localmente
✅ Backtest semanal automático
✅ Reporte de calidad automático
✅ Histórico de 30+ días
✅ Gratis (hasta 2,000 minutos/mes)


═════════════════════════════════════════════════════════════════

¿AHORA QUÉ?

A) Ver workflows en GitHub Actions (2 min, ya)
B) Ejecutar manual ahora (risk-free)
C) Descargar resultados cuando terminen
D) Agregar notificaciones por email
E) Configurar para trading real (requiere más setup)

Responde A, B, C, D o E

═════════════════════════════════════════════════════════════════
