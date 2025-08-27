# Set paths
$routerDir = "app/api/v1"
$mainFile = "app/main.py"

# Read existing main.py content
$mainContent = Get-Content $mainFile -Raw

# Find all router files with APIRouter
$routerFiles = Get-ChildItem -Path $routerDir -Filter *.py | Where-Object {
    (Get-Content $_.FullName -Raw) -match "router\s*=\s*APIRouter"
}

foreach ($file in $routerFiles) {
    $moduleName = $file.BaseName
    $importLine = "from app.api.v1.$moduleName import router as ${moduleName}_router"
    $includeLine = 'app.include_router(' + "${moduleName}_router" + ', prefix="/' + $moduleName + '", tags=["' + $moduleName + '"])'

    if ($mainContent -notmatch [regex]::Escape($importLine)) {
        Add-Content -Path $mainFile -Value "`n$importLine"
    }

    if ($mainContent -notmatch [regex]::Escape($includeLine)) {
        Add-Content -Path $mainFile -Value "`n$includeLine"
    }
}

Write-Host "✅ Routers auto-wired into main.py"