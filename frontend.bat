@echo off
title Volo Health AI - Frontend

color 06
echo.
echo  ==============================================
echo      Volo Health AI  ^|  Frontend Dev Server  
echo      React + Vite  *  Port 5173                 
echo  ==============================================
echo.

:: Change into the Frontend directory
cd /d "%~dp0Frontend"

:: Check node_modules
if not exist "node_modules" (
  color 0C
  echo  [WARN] node_modules not found - running npm install ...
  npm install
  if errorlevel 1 (
    echo  [ERR] npm install failed. Is Node.js on PATH?
    pause
    exit /b 1
  )
)

:: Start Vite dev server
color 0A
echo  [START] Starting Vite on http://localhost:5173
echo  ----------------------------------------------
echo  Press Ctrl+C to stop the server.
echo.
npm run dev

:: If server exits
color 0C
echo.
echo  [STOP] Frontend server stopped.
pause
