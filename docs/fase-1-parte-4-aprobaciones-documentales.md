# Fase 1 - Parte 4 - Aprobaciones documentales

## Objetivo

Agregar gobierno documental sobre las versiones de artefactos del repositorio de procesos.

La meta es que una narrativa, BPMN, evidencia o reporte no sea solo contenido guardado, sino una version con estado, comentarios, decisiones, auditoria y trazabilidad.

## Incluido

- decisiones auditables sobre versiones;
- comentarios por version;
- historial de version;
- transiciones de estado controladas;
- bloqueo indirecto de edicion sobre versiones aprobadas;
- creacion de nuevas versiones sin mutar versiones anteriores;
- UI para revisar, aprobar, rechazar, pedir cambios, publicar y archivar;
- pruebas automatizadas de aprobacion, comentarios e inmutabilidad.

## Estados documentales

```text
draft
in_review
changes_requested
approved
published
superseded
archived
rejected
```

## Acciones implementadas

```text
submit_for_review
request_changes
approve
publish
reject
archive
```

## Reglas de transicion

```text
draft -> in_review | archived
changes_requested -> in_review | archived
in_review -> approved | changes_requested | rejected | archived
approved -> published | archived
published -> archived
rejected -> archived
archived -> sin cambios
```

## Endpoints nuevos

```text
POST /api/process-cases/{case_id}/repository/artifacts/{artifact_id}/versions
POST /api/process-cases/{case_id}/repository/artifact-versions/{version_id}/decisions
POST /api/process-cases/{case_id}/repository/artifact-versions/{version_id}/comments
GET  /api/process-cases/{case_id}/repository/artifact-versions/{version_id}/history
```

## Inmutabilidad

Las versiones no se editan en sitio. Si una version aprobada necesita cambios, se crea una nueva version `draft`.

Esto protege:

- contenido aprobado;
- hash del contenido;
- decisiones humanas;
- historial de revision;
- trazabilidad entre narrativa, BPMN y evidencia.

## Criterio de salida

Esta parte queda completa cuando:

1. una version puede pasar de `draft` a `in_review`;
2. una version en revision puede aprobarse, rechazarse o recibir cambios solicitados;
3. las decisiones quedan guardadas;
4. los comentarios quedan guardados;
5. el historial muestra version, decisiones y comentarios;
6. una nueva version no modifica la version aprobada anterior;
7. backend y frontend pasan sus verificaciones.

## Siguiente parte

La Parte 5 implementa:

- comparacion basica entre versiones de texto;
- vista de diferencias;
- marcas de evidencia por artefacto;
- relacion entre actividades BPMN y evidencia;
- primeras reglas de calidad documental.
