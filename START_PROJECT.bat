@echo off
chcp 65001 >nul
title Start Document Chatbot
echo ========================================
echo   Starting Document Chatbot (Backend + Frontend)
echo ========================================
echo.
echo Opening Backend window (http://127.0.0.1:8000)...
start "Document Chatbot - Backend" cmd /k "cd /d "%~dp0" && call START_BACKEND.bat"
echo.
echo Opening Frontend window (http://localhost:3000)...
start "Document Chatbot - Frontend" cmd /k "cd /d "%~dp0" && call START_FRONTEND.bat"
echo.
echo Both servers are starting in separate windows.
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://localhost:3000
echo.
echo Close this window when done. Keep the Backend and Frontend windows open.
pause
