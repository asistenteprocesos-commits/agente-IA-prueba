# Fase 1 - Parte 5 - Trazabilidad y calidad documental

## Objetivo

Agregar comparacion de versiones, evidencias vinculadas y reglas iniciales de calidad documental.

Esta parte convierte el repositorio en algo mas util para supervision: no basta con aprobar una version; tambien debemos ver que cambio, que evidencia la respalda y que tan completa esta.

## Incluido

- creacion de nuevas versiones para un artefacto;
- comparacion textual entre dos versiones;
- conteo de lineas agregadas y eliminadas;
- registro de evidencias por version;
- vinculacion opcional de evidencia con actividad del proceso;
- evaluacion inicial de calidad documental;
- UI para crear versiones, comparar, registrar evidencia y ver score;
- pruebas automatizadas de diff, evidencia y calidad.

## Endpoints nuevos

```text
GET  /api/process-cases/{case_id}/repository/artifact-versions/{base_version_id}/diff/{target_version_id}
POST /api/process-cases/{case_id}/repository/artifact-versions/{version_id}/evidence
GET  /api/process-cases/{case_id}/repository/artifact-versions/{version_id}/evidence
GET  /api/process-cases/{case_id}/repository/artifact-versions/{version_id}/quality
```

## Evidencias

Tipos iniciales:

```text
interview
document
event_log
process_mining
bpmn_activity
decision
other
```

Cada evidencia registra:

- tipo;
- fuente;
- extracto;
- actividad relacionada opcional;
- URL opcional;
- notas.

## Calidad documental inicial

Reglas implementadas:

1. `minimum_detail`: contenido con detalle minimo.
2. `has_actor`: menciona actor, rol o area.
3. `has_flow_signal`: muestra secuencia o accion de flujo.
4. `has_evidence`: tiene evidencia vinculada.

El score actual es una primera heuristica. En fases posteriores se reemplazara o complementara con evaluaciones mas avanzadas usando RAG, reglas BPMN y validacion humana.

## Criterio de salida

Esta parte queda completa cuando:

1. se puede crear una segunda version;
2. se puede comparar contra la version anterior;
3. se puede registrar evidencia;
4. se puede ver evidencia vinculada;
5. se calcula score de calidad;
6. frontend y backend pasan verificaciones.

## Siguiente parte

La Parte 6 implementa ingestion documental:

- carga de documentos fuente;
- metadata;
- extraccion de texto;
- almacenamiento inicial;
- fragmentacion para preparar embeddings y RAG de la Fase 2.
