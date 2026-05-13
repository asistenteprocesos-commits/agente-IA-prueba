$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$BackendPort = 8010
$FrontendPort = 5173
$NodeDir = Get-ChildItem -Path (Join-Path $Root ".tools") -Directory -Filter "node-v*-win-x64" -ErrorAction SilentlyContinue |
    Sort-Object Name -Descending |
    Select-Object -First 1

if (-not $NodeDir) {
    throw "No local Node.js runtime found in .tools. Ejecuta scripts\install-node-portable.cmd primero."
}

& (Join-Path $PSScriptRoot "stop-dev-servers.ps1")
& (Join-Path $PSScriptRoot "start-ollama.cmd")

$Logs = Join-Path $Root "storage\logs"
New-Item -ItemType Directory -Force $Logs | Out-Null

$BackendCommand = @"
Set-Location -LiteralPath '$Root'
& '.\.venv\Scripts\python.exe' -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port $BackendPort *> '.\storage\logs\backend-$BackendPort.log'
"@

$FrontendCommand = @"
`$env:Path = '$($NodeDir.FullName);' + `$env:Path
`$env:VITE_API_BASE_URL = 'http://127.0.0.1:$BackendPort'
Set-Location -LiteralPath '$Root\frontend'
& '..\.tools\$($NodeDir.Name)\node.exe' '.\node_modules\vite\bin\vite.js' --host 127.0.0.1 --port $FrontendPort *> '..\storage\logs\frontend-5173.log'
"@

Start-Process -WindowStyle Hidden -FilePath powershell -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $BackendCommand
Start-Process -WindowStyle Hidden -FilePath powershell -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $FrontendCommand

Start-Sleep -Seconds 5

Write-Host "Backend:  http://127.0.0.1:$BackendPort/api/health"
Write-Host "API docs: http://127.0.0.1:$BackendPort/api/docs"
Write-Host "Frontend: http://127.0.0.1:$FrontendPort"
