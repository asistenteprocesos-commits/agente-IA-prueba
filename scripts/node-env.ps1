$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$LocalNode = Get-ChildItem -Path (Join-Path $Root ".tools") -Directory -Filter "node-v*-win-x64" -ErrorAction SilentlyContinue |
    Sort-Object Name -Descending |
    Select-Object -First 1

if (-not $LocalNode) {
    throw "No local Node.js runtime found in .tools. Install it before running frontend commands."
}

$env:Path = "$($LocalNode.FullName);$env:Path"
node --version
npm.cmd --version
