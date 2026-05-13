# Fase 1 - Parte 3 - Persistencia y repositorio inicial

## Objetivo

Convertir el primer dominio del MVP en una base persistente y crear el repositorio documental inicial por caso de proceso.

Esta parte deja de usar almacenamiento en memoria. Los casos ya se guardan en base de datos y cada caso crea automaticamente su repositorio documental.

## Incluido

- capa SQLAlchemy;
- base SQLite local por defecto;
- preparacion para PostgreSQL mediante `DATABASE_URL`;
- tabla `process_cases`;
- tabla `process_repositories`;
- tabla `process_artifacts`;
- tabla `artifact_versions`;
- creacion automatica de repositorio al crear un caso;
- endpoint para consultar repositorio;
- endpoint para listar artefactos;
- endpoint para crear artefacto con primera version;
- frontend conectado al repositorio;
- pruebas automatizadas de persistencia y versionado inicial.

## Endpoints nuevos

```text
GET  /api/process-cases/{case_id}/repository
GET  /api/process-cases/{case_id}/repository/artifacts
POST /api/process-cases/{case_id}/repository/artifacts
```

## Base de datos

Por defecto:

```text
sqlite:///./storage/app.db
```

Variable configurable:

```text
DATABASE_URL=sqlite:///./storage/app.db
```

Cuando pasemos a PostgreSQL, el cambio debe hacerse por configuracion:

```text
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/agente_ia
```

## Repositorio documental inicial

Al crear un caso se crea:

```text
ProcessCase -> ProcessRepository
```

Luego el usuario puede crear artefactos:

```text
ProcessRepository -> ProcessArtifact -> ArtifactVersion
```

La primera version queda en estado:

```text
draft
```

## Tipos de artefactos iniciales

- `process_narrative_as_is`
- `process_narrative_to_be`
- `bpmn_xml_as_is`
- `bpmn_xml_to_be`
- `interview_notes`
- `transcript`
- `event_log`
- `mining_report`
- `simulation_parameters`
- `simulation_result`
- `improvement_report`
- `final_report`
- `presentation`

## Decisiones tecnicas

- SQLite local para avanzar sin instalar servidor de base de datos.
- SQLAlchemy para mantener el dominio portable.
- Versiones de artefactos con hash SHA-256 del contenido.
- Versiones aprobadas y bloqueo de edicion se implementaran en una parte posterior.

## Criterio de salida

Esta parte queda completa cuando:

1. los casos sobreviven al reinicio del backend;
2. cada caso tiene repositorio documental;
3. se puede crear un artefacto con primera version;
4. el frontend muestra repositorio y artefactos;
5. las pruebas backend pasan;
6. el frontend compila.

## Siguiente parte

La Parte 4 implementa:

- estados documentales completos;
- aprobacion/rechazo de versiones;
- bloqueo de versiones aprobadas;
- historial visible de cambios.

La comparacion basica de versiones queda para la Parte 5.
