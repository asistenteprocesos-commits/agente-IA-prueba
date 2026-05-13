@echo off
setlocal

where ollama >nul 2>nul
if not %ERRORLEVEL%==0 (
  echo Ollama no esta instalado o no esta en PATH.
  echo Ejecuta scripts\install-ollama.cmd
  exit /b 1
)

ollama list >nul 2>nul
if %ERRORLEVEL%==0 (
  echo Ollama ya esta respondiendo en http://127.0.0.1:11434
  exit /b 0
)

start "Ollama local server" /min ollama serve
echo Ollama iniciandose en http://127.0.0.1:11434
