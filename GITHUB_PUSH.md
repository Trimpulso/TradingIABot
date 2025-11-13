📤 INSTRUCCIONES PARA DESPLEGAR EN GITHUB
═════════════════════════════════════════════════════════════════

El repositorio Git local ya está configurado y listo para GitHub.

PASO 1: Crear token de acceso personal en GitHub
───────────────────────────────────────────────

1. Ve a: https://github.com/settings/tokens
2. Haz clic en "Generate new token (classic)"
3. Selecciona permisos:
   ✓ repo (acceso completo)
   ✓ workflow (si usarás CI/CD)
4. Copia el token (aparece solo una vez)
5. Guarda en lugar seguro

PASO 2: Autenticar Git con GitHub
──────────────────────────────────

Opción A: Usar Personal Access Token (recomendado)
────────────────────────────────────────────────
git config --global credential.helper wincred

Luego cuando hagas git push:
- Username: tu_usuario_github
- Password: el_token_que_copiaste


Opción B: Configurar SSH (alternativa)
───────────────────────────────────────
# Generar clave SSH
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Copiar clave pública a GitHub
# https://github.com/settings/keys


PASO 3: Hacer push al repositorio remoto
──────────────────────────────────────────

En PowerShell, ejecuta:

cd "c:\github\Trading IA Bot"
git push -u origin master

Si pide autenticación:
- Username: tu_usuario_github  (ej: Trimpulso)
- Password: tu_personal_access_token


PASO 4: Verificar en GitHub
────────────────────────────

Ve a: https://github.com/Trimpulso/TradingIABot

Deberías ver:
✓ 17 archivos
✓ Estructura completa de carpetas
✓ Documentación README.md


PASO 5: Configurar GitHub (opcional pero recomendado)
──────────────────────────────────────────────────────

1. Descripción del repositorio:
   "ML-powered crypto trading bot with Freqtrade"

2. Topics (etiquetas):
   - trading
   - machine-learning
   - freqtrade
   - cryptocurrency
   - python
   - bot

3. Estructura de README:
   ✓ Ya incluida en README.md

4. License (opcional):
   - MIT (educativo)
   - GPL v3 (código abierto)

5. GitHub Pages (opcional):
   - Para documentación adicional


COMANDOS GIT ÚTILES
═══════════════════

Ver estado actual:
  git status

Ver commits:
  git log --oneline
  git log --graph --all --decorate

Ver cambios sin commitear:
  git diff

Deshacer cambios:
  git reset --hard HEAD

Crear rama nueva:
  git checkout -b feature/nombre-feature
  git push -u origin feature/nombre-feature


⚠️  IMPORTANTE ANTES DE HACER PUSH
═════════════════════════════════

1. Verificar que .env NO esté commiteado:
   ✓ Ya está en .gitignore

2. No incluir datos sensibles:
   ✓ Archivos de configuración seguros

3. Archivos grandes excluidos:
   ✓ data/ y models/ están en .gitignore


WORKFLOW RECOMENDADO FUTURO
════════════════════════════

1. Desarrollo local:
   git checkout -b feature/nueva-caracteristica

2. Hacer cambios y commits:
   git add .
   git commit -m "Descripción del cambio"

3. Push a rama:
   git push -u origin feature/nueva-caracteristica

4. En GitHub: Create Pull Request

5. Merge a master cuando esté aprobado:
   git checkout master
   git pull origin master
   git merge feature/nueva-caracteristica
   git push origin master


═════════════════════════════════════════════════════════════════

¿Preguntas?

Los comandos están listos para ejecutar. Solo necesitas:
1. Token de GitHub
2. Ejecutar: git push -u origin master

¡Listo para desplegar! 🚀
