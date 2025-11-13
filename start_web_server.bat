@echo off
REM Script para iniciar el servidor web del chatbot

echo.
echo ========================================
echo  TRADING IA BOT - WEB SERVER
echo ========================================
echo.

cd /d C:\github\Trading IA Bot

echo Activando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo Iniciando servidor Flask...
echo.
echo Abre tu navegador en: http://127.0.0.1:5000
echo.

python gemini_web_server.py

pause
