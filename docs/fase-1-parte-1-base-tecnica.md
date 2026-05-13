# Fase 1 - Parte 1 - Base tecnica

## Objetivo

Crear una base ejecutable y verificable para empezar el MVP sin mezclar todavia casos de proceso, repositorio documental, IA o BPMN.

## Incluido

- estructura `backend`;
- API `FastAPI`;
- endpoint `GET /api/health`;
- configuracion por variables de entorno;
- CORS para frontend local;
- prueba automatizada del health check;
- estructura `frontend`;
- pantalla React/Vite conectada al backend;
- scripts de arranque local.

## No incluido en esta parte

- base de datos;
- autenticacion;
- gestion de casos;
- repositorio documental;
- ingestion de documentos;
- agentes IA;
- BPMN;
- process mining.

## Comandos

Backend:

```powershell
.\scripts\start-backend.cmd
```

Frontend:

```powershell
.\scripts\start-frontend.cmd
```

## URLs

```text
Backend:  http://127.0.0.1:8000/api/health
Docs API: http://127.0.0.1:8000/api/docs
Frontend: http://127.0.0.1:5173
```

## Criterio de salida

Esta parte queda completa cuando:

1. el backend responde `status=ok`;
2. la prueba automatizada del backend pasa;
3. el frontend puede instalar dependencias y levantar cuando Node.js este disponible;
4. la documentacion indica como ejecutar ambos servicios.

## Siguiente parte

La Parte 2 debe crear:

- modelo inicial `ProcessCase`;
- estructura de persistencia;
- primer endpoint para crear y listar casos;
- pantalla simple de tablero de casos.
