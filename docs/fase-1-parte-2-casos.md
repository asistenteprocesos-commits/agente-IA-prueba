# Fase 1 - Parte 2 - Casos de proceso

## Objetivo

Crear el primer dominio funcional del MVP: `ProcessCase`.

Esta parte permite crear y listar casos de proceso. Es la base sobre la que despues se conectaran documentos, entrevistas, BPMN, repositorio versionado, process mining y aprobaciones.

## Incluido

- endpoints backend para casos;
- esquema `ProcessCase`;
- estados iniciales del caso;
- almacenamiento temporal en memoria;
- pruebas automatizadas;
- tablero frontend de casos;
- formulario para crear caso;
- Node.js portable para ejecutar frontend sin permisos de administrador.

## Endpoints

```text
GET  /api/process-cases
POST /api/process-cases
GET  /api/process-cases/{case_id}
```

## Estado de almacenamiento

Por ahora los casos se guardan en memoria. Esto permite validar la API y la interfaz.

La siguiente parte debe migrar esto a persistencia real con `PostgreSQL` o, si necesitamos acelerar localmente, `SQLite` como paso intermedio.

## Criterio de salida

Esta parte queda completa cuando:

1. el backend crea y lista casos;
2. las pruebas pasan;
3. el frontend compila;
4. la UI permite crear un caso;
5. queda claro donde se conectara la base de conocimiento.

## Base de conocimiento y ML

Los libros y la parte de machine learning no entran en este modulo. Se conectaran desde la Fase 2 mediante:

- ingestion documental;
- fragmentacion semantica;
- metadata;
- embeddings;
- Qdrant;
- RAG con citas;
- evaluaciones de calidad de recuperacion.

La decision tecnica queda en `ADR 004 - Base de conocimiento y machine learning`.

## Siguiente parte

La Parte 3 debe crear persistencia y repositorio inicial:

- configuracion de base de datos;
- migraciones;
- tabla `process_cases`;
- tabla inicial `process_repositories`;
- API para repositorio documental basico.
