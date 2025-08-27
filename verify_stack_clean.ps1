Write-Host "`n🚀 Starting Full Stack Verification..." -ForegroundColor Cyan

# Step 1: Launch FastAPI Server
Write-Host "`n🔧 Launching FastAPI server..." -ForegroundColor Yellow
Start-Process "python" "main.py"
Start-Sleep -Seconds 3

# Step 2: Check Router Wiring
Write-Host "`n📡 Verifying router endpoints..." -ForegroundColor Yellow
$routes = Invoke-RestMethod -Uri "http://localhost:8000/docs" -ErrorAction SilentlyContinue
if ($routes) {
    Write-Host "✅ Router wiring looks good." -ForegroundColor Green
} else {
    Write-Host "❌ Router wiring failed. Check FastAPI logs." -ForegroundColor Red
    exit 1
}

# Step 3: DB Health Check
Write-Host "`n🧠 Checking DB health..." -ForegroundColor Yellow
$dbStatus = Invoke-RestMethod -Uri "http://localhost:8000/health/db" -ErrorAction SilentlyContinue
if ($dbStatus.status -eq "ok") {
    Write-Host "✅ DB is healthy." -ForegroundColor Green
} else {
    Write-Host "❌ DB check failed. Investigate DB service." -ForegroundColor Red
    exit 1
}

# Step 4: Smoke Test Key Endpoint
Write-Host "`n🔥 Running smoke test on /ping..." -ForegroundColor Yellow
$ping = Invoke-RestMethod -Uri "http://localhost:8000/ping" -ErrorAction SilentlyContinue
if ($ping -eq "pong") {
    Write-Host "✅ Endpoint /ping responded correctly." -ForegroundColor Green
} else {
    Write-Host "❌ Smoke test failed. Endpoint not responding." -ForegroundColor Red
    exit 1
}

Write-Host "`nStack verification complete. All systems go!" -ForegroundColor Cyan
