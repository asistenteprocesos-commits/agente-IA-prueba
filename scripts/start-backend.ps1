$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    python -m venv (Join-Path $Root ".venv")
}

& $VenvPython -m pip install -r (Join-Path $Root "backend\requirements.txt")
& $VenvPython -m uvicorn app.main:app --reload --app-dir (Join-Path $Root "backend") --host 127.0.0.1 --port 8000
