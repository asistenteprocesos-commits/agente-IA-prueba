@echo off
setlocal

where ollama >nul 2>nul
if not %ERRORLEVEL%==0 (
  echo Ollama no esta instalado o no esta en PATH.
  echo Ejecuta scripts\install-ollama.cmd
  exit /b 1
)

set "REASONING_MODEL=%OLLAMA_REASONING_MODEL%"
if "%REASONING_MODEL%"=="" set "REASONING_MODEL=deepseek-r1:1.5b"

set "EMBEDDING_MODEL=%OLLAMA_EMBEDDING_MODEL%"
if "%EMBEDDING_MODEL%"=="" set "EMBEDDING_MODEL=qwen3-embedding:0.6b"

call "%~dp0start-ollama.cmd"

echo Descargando modelo de razonamiento: %REASONING_MODEL%
ollama pull "%REASONING_MODEL%"
if not %ERRORLEVEL%==0 exit /b %ERRORLEVEL%

echo Descargando modelo de embeddings: %EMBEDDING_MODEL%
ollama pull "%EMBEDDING_MODEL%"
if not %ERRORLEVEL%==0 exit /b %ERRORLEVEL%

ollama list
