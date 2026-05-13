@echo off
setlocal

set "ROOT=%~dp0.."
set "NODE_VERSION=24.15.0"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop';" ^
  "$root=(Resolve-Path '%ROOT%').Path;" ^
  "$tools=Join-Path $root '.tools';" ^
  "$version='%NODE_VERSION%';" ^
  "$zipName='node-v' + $version + '-win-x64.zip';" ^
  "$zipPath=Join-Path $tools $zipName;" ^
  "$nodeDir=Join-Path $tools ('node-v' + $version + '-win-x64');" ^
  "New-Item -ItemType Directory -Force -Path $tools | Out-Null;" ^
  "if (-not (Test-Path $zipPath)) { Invoke-WebRequest -Uri ('https://nodejs.org/dist/v' + $version + '/' + $zipName) -OutFile $zipPath };" ^
  "if (-not (Test-Path $nodeDir)) { Expand-Archive -LiteralPath $zipPath -DestinationPath $tools };" ^
  "& (Join-Path $nodeDir 'node.exe') --version;" ^
  "& (Join-Path $nodeDir 'npm.cmd') --version;"
