# NoteGuard AI - PowerShell Launcher
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "          Starting NoteGuard AI Local Environment                     " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Start Backend in separate window
Write-Host "[*] Launching Backend on http://127.0.0.1:8000..." -ForegroundColor Green
Start-Process cmd -ArgumentList "/k", "cd /d `"$scriptDir\backend`" && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Start-Sleep -Seconds 4

# 2. Start Frontend in separate window
Write-Host "[*] Launching Frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process cmd -ArgumentList "/k", "cd /d `"$scriptDir\frontend`" && npm run dev"

Start-Sleep -Seconds 3

# 3. Open browser
Write-Host "[*] Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

Write-Host "NoteGuard AI is running! Close the opened terminal windows to stop." -ForegroundColor Cyan
