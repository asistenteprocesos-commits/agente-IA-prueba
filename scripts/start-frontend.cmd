@echo off
setlocal

set "ROOT=%~dp0.."
set "NODE_DIR="

for /d %%D in ("%ROOT%\.tools\node-v*-win-x64") do set "NODE_DIR=%%~fD"

if "%NODE_DIR%"=="" (
  echo No local Node.js runtime found in .tools.
  exit /b 1
)

set "PATH=%NODE_DIR%;%PATH%"
cd /d "%ROOT%\frontend"
npm.cmd install
npm.cmd run dev
