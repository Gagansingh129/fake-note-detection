# NoteGuard AI - PowerShell Launcher
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "          Starting NoteGuard AI Local Environment                     " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Start Backend in separate window
Write-Host "[*] Launching Backend on http://127.0.0.1:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Start-Sleep -Seconds 3

# 2. Start Frontend in separate window
Write-Host "[*] Launching Frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Start-Sleep -Seconds 2

# 3. Open browser
Write-Host "[*] Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

Write-Host "NoteGuard AI is running! Press Ctrl+C in the popped up windows to stop." -ForegroundColor Cyan
