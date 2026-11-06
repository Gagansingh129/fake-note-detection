@echo off
title NoteGuard AI - Local Server Launcher
echo ======================================================================
echo           Starting NoteGuard AI Local Environment
echo ======================================================================
echo.

:: Check python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in system PATH.
    pause
    exit /b 1
)

:: Check node
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in system PATH.
    pause
    exit /b 1
)

echo [*] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "NoteGuard Backend (FastAPI)" cmd /k "cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [*] Waiting 3 seconds for backend models to load...
timeout /t 3 /nobreak >nul

echo [*] Starting React + Vite Frontend on http://localhost:5173 ...
start "NoteGuard Frontend (React + Vite)" cmd /k "cd frontend && npm run dev"

echo [*] Opening NoteGuard AI in your web browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173

echo.
echo ======================================================================
echo   NoteGuard AI is now running!
echo   Frontend : http://localhost:5173
echo   Backend  : http://127.0.0.1:8000/docs (Swagger API Docs)
echo ======================================================================
echo.
pause
