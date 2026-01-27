@echo off
chcp 65001 >nul
title Document Chatbot Frontend
color 0B
echo ========================================
echo   Document Chatbot Frontend
echo ========================================
echo.
cd /d "%~dp0frontend"
echo Current directory: %CD%
echo.
echo Checking for node_modules...
if not exist "node_modules" (
    echo node_modules not found. Installing dependencies...
    call npm install
    echo.
)
echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:3000
echo Press CTRL+C to stop the server
echo.
call npm start
pause

