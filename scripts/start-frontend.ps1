$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Frontend = Join-Path $Root "frontend"
$LocalNode = Get-ChildItem -Path (Join-Path $Root ".tools") -Directory -Filter "node-v*-win-x64" -ErrorAction SilentlyContinue |
    Sort-Object Name -Descending |
    Select-Object -First 1

if ($LocalNode) {
    $env:Path = "$($LocalNode.FullName);$env:Path"
}

Set-Location $Frontend
npm.cmd install
npm.cmd run dev
