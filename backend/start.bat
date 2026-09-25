@echo off
title SecureAI Labs Backend
color 0A
echo.
echo  ==========================================
echo   SecureAI Labs Backend Server
echo  ==========================================
echo.
echo  Starting...
echo.

cd /d "%~dp0"
python app.py

echo.
echo  Server stopped.
pause
