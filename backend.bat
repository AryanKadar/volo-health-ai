@echo off
title Volo Health AI - Backend

:: ──────────────────────────────────────────────
::  Color codes:  0A = Black bg / Green fg
::                0C = Black bg / Red fg
::                0B = Black bg / Cyan fg
:: ──────────────────────────────────────────────

color 0A
echo.
echo  ==============================================
echo      Volo Health AI  ^|  Backend Server      
echo      FastAPI  *  Port 8000  *  Azure OpenAI     
echo  ==============================================
echo.

:: Change into the Backend directory
cd /d "%~dp0Backend"

:: Check venv exists, create if not
if not exist "venv\Scripts\activate.bat" (
  color 0C
  echo  [WARN] Virtual environment not found - creating one ...
  python -m venv venv
  if errorlevel 1 (
    echo  [ERR] Failed to create venv. Is Python on PATH?
    pause
    exit /b 1
  )
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install / upgrade dependencies silently if requirements.txt changed
echo  [*] Installing / verifying dependencies ...
pip install -r requirements.txt --quiet
echo  [OK] Dependencies ready.
echo.

:: Start FastAPI
color 0B
echo  [START] Starting FastAPI on http://localhost:8000
echo  ----------------------------------------------
echo  Press Ctrl+C to stop the server.
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

:: If server exits
color 0C
echo.
echo  [STOP] Backend server stopped.
pause
