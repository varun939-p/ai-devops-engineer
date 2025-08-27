param(
    [string]$SyntheticLog = ".\synthetic-events.log",
    [string]$WatchdogLog  = ".\watchdog-alerts.log"
)

if (!(Test-Path $SyntheticLog)) { Write-Host "Synthetic log not found: $SyntheticLog" -ForegroundColor Red; return }
if (!(Test-Path $WatchdogLog)) { Write-Host "Watchdog log not found: $WatchdogLog" -ForegroundColor Red; return }

$syntheticEvents = Get-Content $SyntheticLog | Where-Object {$_ -match "^\[\d{2}:\d{2}:\d{2}\]"}
$watchdogEvents  = Get-Content $WatchdogLog

Write-Host "=== Comparing $(($syntheticEvents).Count) injected events to watchdog output ===" -ForegroundColor Cyan

$missed = @()

foreach ($event in $syntheticEvents) {
    if (-not ($watchdogEvents -match [regex]::Escape($event))) {
        $missed += $event
    }
}

if ($missed.Count -eq 0) {
    Write-Host "? All synthetic events were detected by the watchdog" -ForegroundColor Green
} else {
    Write-Host "? Missed events ($($missed.Count)):" -ForegroundColor Red
    $missed | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
}