@echo off
setlocal

where ollama >nul 2>nul
if %ERRORLEVEL%==0 (
  ollama --version
  exit /b 0
)

where winget >nul 2>nul
if not %ERRORLEVEL%==0 (
  echo No se encontro winget. Instala Ollama manualmente desde https://ollama.com/download/windows
  exit /b 1
)

winget install -e --id Ollama.Ollama
