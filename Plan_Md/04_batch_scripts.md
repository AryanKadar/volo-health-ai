# 04 – Batch Scripts

## Overview
Two batch files at the project root (`intern/`) launch each service.  
They activate the correct environment, show color-coded status, and block until the server exits.

---

## `backend.bat` (at `intern/backend.bat`)

```batch
@echo off
title Volo Health AI – Backend

:: ──────────────────────────────────────────────
::  Color codes:  0A = Black bg / Green fg
::                0C = Black bg / Red fg
::                0B = Black bg / Cyan fg
:: ──────────────────────────────────────────────

color 0A
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   🏥  Volo Health AI  │  Backend Server      ║
echo  ║   FastAPI  •  Port 8000  •  Azure OpenAI     ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: Change into the Backend directory
cd /d "%~dp0Backend"

:: Check venv exists, create if not
if not exist "venv\Scripts\activate.bat" (
  color 0C
  echo  ⚠  Virtual environment not found – creating one …
  python -m venv venv
  if errorlevel 1 (
    echo  ✖  Failed to create venv. Is Python on PATH?
    pause
    exit /b 1
  )
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install / upgrade dependencies silently if requirements.txt changed
echo  📦  Installing / verifying dependencies …
pip install -r requirements.txt --quiet
echo  ✔  Dependencies ready.
echo.

:: Start FastAPI
color 0B
echo  🚀  Starting FastAPI on http://localhost:8000
echo  ──────────────────────────────────────────────
echo  Press Ctrl+C to stop the server.
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

:: If server exits
color 0C
echo.
echo  ✖  Backend server stopped.
pause
```

---

## `frontend.bat` (at `intern/frontend.bat`)

```batch
@echo off
title Volo Health AI – Frontend

color 06
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   ⚡  Volo Health AI  │  Frontend Dev Server  ║
echo  ║   React + Vite  •  Port 5173                 ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: Change into the Frontend directory
cd /d "%~dp0Frontend"

:: Check node_modules
if not exist "node_modules" (
  color 0C
  echo  ⚠  node_modules not found – running npm install …
  npm install
  if errorlevel 1 (
    echo  ✖  npm install failed. Is Node.js on PATH?
    pause
    exit /b 1
  )
)

:: Start Vite dev server
color 0A
echo  🚀  Starting Vite on http://localhost:5173
echo  ──────────────────────────────────────────────
echo  Press Ctrl+C to stop the server.
echo.
npm run dev

:: If server exits
color 0C
echo.
echo  ✖  Frontend server stopped.
pause
```

---

## Terminal Output Guide

| Color   | Meaning                         |
|---------|---------------------------------|
| 🟢 Green | Server ready / success          |
| 🔵 Cyan  | Server starting / informational  |
| 🟡 Yellow| Frontend dev mode               |
| 🔴 Red   | Error / warning                 |

---

## How to Run

1. Open a terminal in `intern/` (or double-click `.bat`).
2. Run backend first: `backend.bat`
3. Open a second terminal: `frontend.bat`
4. Visit `http://localhost:5173`
