# Backend

API base del MVP para `agente ia prueba`.

## Ejecutar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

## Base de datos

Por defecto usa SQLite local:

```text
sqlite:///./storage/app.db
```

Puedes cambiarlo con:

```text
DATABASE_URL=sqlite:///./storage/app.db
```
