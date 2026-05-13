$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Frontend = Join-Path $Root "frontend"
$LocalNode = Get-ChildItem -Path (Join-Path $Root ".tools") -Directory -Filter "node-v*-win-x64" -ErrorAction SilentlyContinue |
    Sort-Object Name -Descending |
    Select-Object -First 1

if ($LocalNode) {
    $env:Path = "$($LocalNode.FullName);$env:Path"
}

if (-not $env:VITE_API_BASE_URL) {
    $env:VITE_API_BASE_URL = "http://127.0.0.1:8010"
}

Set-Location $Frontend
npm.cmd install
npm.cmd run dev
