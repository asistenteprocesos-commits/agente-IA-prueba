# ════════════════════════════════════════════════════════════════════════
# Setup PC Pruebas — Agente BPMS
# Instala dependencias e inicializa base de datos.
# NOTA: Este script NO descarga modelos de Ollama.
# Para descargar modelos, ejecuta: scripts\pull-local-llm-models.cmd
# ════════════════════════════════════════════════════════════════════════

Write-Host "Iniciando configuracion de PC de pruebas..." -ForegroundColor Cyan

# 1. Frontend
Write-Host "1. Instalando dependencias del Frontend..." -ForegroundColor Yellow
Set-Location "frontend"
npm install
Set-Location ".."

# 2. Backend
Write-Host "2. Instalando dependencias del Backend..." -ForegroundColor Yellow
Set-Location "backend"
# Crear entorno virtual si no existe
if (-Not (Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Base de datos
Write-Host "3. Inicializando Base de Datos..." -ForegroundColor Yellow
# Usamos un script python rapido para crear las tablas
$initDbScript = @"
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from app.db.session import init_db
init_db()
print('Base de datos inicializada correctamente.')
"@
Out-File -FilePath "init_db.py" -InputObject $initDbScript -Encoding UTF8
python init_db.py

Set-Location ".."

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Configuracion completada con exito." -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Siguientes pasos:"
Write-Host "1. Edita 'backend\.env' y coloca tus API Keys de Gemini y Groq."
Write-Host "2. Ejecuta 'scripts\start-backend.cmd' para levantar el servidor backend."
Write-Host "3. Ejecuta 'scripts\start-frontend.cmd' para levantar la web."
Write-Host "4. Si usaras modelos locales, instala Ollama y ejecuta 'scripts\pull-local-llm-models.cmd'"
