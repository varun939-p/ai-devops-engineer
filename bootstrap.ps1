Write-Host "Bootstrapping Dev Environment..."

#Step 1: Wire routers
.\auto_wire_routers.ps1

#Step 2: Launch FastAPI server
Write-Host "Starting FastAPI server..."
Start-process "cmd.exe" -ArgumentList "/c uvicorn app.main:app --reload"

Write-Host "Dev environment is live"
