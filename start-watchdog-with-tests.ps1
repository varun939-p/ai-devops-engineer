param(
    [switch]$StopAll,
    [int]$IntervalSeconds = 5,
    [ValidateSet("single","multi","mixed")]
    [string]$StartMode = "mixed",
    [int]$SwitchEvery = 30,
    [string]$LogFile = ".\synthetic-events.log"
)

$watchdogTitle = "watchdog.ps1"

if ($StopAll) {
    Write-Host "=== Stopping watchdog and injector processes ===" -ForegroundColor Cyan
    Get-Process powershell -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowTitle -match $watchdogTitle -or $_.MainWindowTitle -match "start-watchdog-with-tests.ps1" } |
        ForEach-Object {
            Write-Host "Stopping PID $($_.Id) - $($_.MainWindowTitle)" -ForegroundColor Yellow
            Stop-Process -Id $_.Id -Force
        }
    return
}

Write-Host "=== Launching watchdog and adaptive test log injection ===" -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `"& { .\watchdog.ps1 }`"" -WindowStyle Normal
Start-Sleep -Seconds 2

$testMessages = @{
    single = @("Error: Database unreachable", "Warning: High CPU load")
    multi  = @("CRITICAL: Disk space low - server1", "ALERT: Memory leak detected in process XYZ")
    mixed  = @("Error: API timeout", "CRITICAL: Disk space low", "Warning: High CPU", "ALERT: Service restart triggered")
}

$keywordModes = $testMessages.Keys
$KeywordMode = $StartMode
$lastSwitch = Get-Date

Write-Host "Injecting every $IntervalSeconds sec — starting in '$KeywordMode', switching every $SwitchEvery sec" -ForegroundColor Yellow
Write-Host "Logging to: $LogFile" -ForegroundColor Green
Add-Content -Path $LogFile -Value "=== New Session $(Get-Date) ==="

while ($true) {
    if ((New-TimeSpan -Start $lastSwitch).TotalSeconds -ge $SwitchEvery) {
        $KeywordMode = Get-Random $keywordModes
        $lastSwitch = Get-Date
        Write-Host "*** Mode switched to '$KeywordMode' ***" -ForegroundColor Magenta
        Add-Content -Path $LogFile -Value "*** Mode switched to '$KeywordMode' @ $(Get-Date -Format 'HH:mm:ss') ***"
    }
    $msg = Get-Random $testMessages[$KeywordMode]
    $timestamp = Get-Date -Format 'HH:mm:ss'
    $line = "[$timestamp] $msg"
    Write-Host $line -ForegroundColor Yellow
    Add-Content -Path $LogFile -Value $line
    Start-Sleep -Seconds $IntervalSeconds
}