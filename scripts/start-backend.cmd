@echo off
setlocal

set "ROOT=%~dp0.."
set "PYTHON=%ROOT%\.venv\Scripts\python.exe"
if "%BACKEND_PORT%"=="" set "BACKEND_PORT=8010"

if not exist "%PYTHON%" (
  python -m venv "%ROOT%\.venv"
)

"%PYTHON%" -m pip install -r "%ROOT%\backend\requirements.txt"
"%PYTHON%" -m uvicorn app.main:app --reload --app-dir "%ROOT%\backend" --host 127.0.0.1 --port %BACKEND_PORT%
