$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Ports = @(8000, 8001, 8002, 8003, 8004, 8010, 8011, 8012, 5173, 5174, 5175, 5176, 5177, 5178)

$ProcessIds = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalPort -in $Ports } |
    Select-Object -ExpandProperty OwningProcess -Unique

if (-not $ProcessIds) {
    Write-Host "No hay servidores de desarrollo activos para detener."
    exit 0
}

$Processes = Get-CimInstance Win32_Process |
    Where-Object {
        $_.ProcessId -in $ProcessIds -and
        $_.CommandLine -and
        (
            $_.CommandLine.Contains($ProjectRoot) -or
            $_.CommandLine.Contains("uvicorn app.main:app") -or
            $_.CommandLine.Contains("vite")
        )
    }

foreach ($Process in $Processes) {
    Write-Host "Deteniendo PID $($Process.ProcessId): $($Process.Name)"
    Stop-Process -Id $Process.ProcessId -Force
}

Write-Host "Servidores de desarrollo del proyecto detenidos."
