# Fase 1 - Parte 8 - Extraccion as-is

## Objetivo

Convertir notas de entrevistas en elementos estructurados del proceso actual.

Hasta la Parte 7 el sistema guardaba participantes, sesiones y notas. En esta parte empieza la transformacion hacia modelo de proceso: actividades, eventos, roles, reglas, sistemas, entradas, salidas, excepciones, dolores, oportunidades, metricas y controles.

## Incluido

- tabla de elementos `as-is` por caso;
- vinculacion opcional con entrevista fuente;
- captura manual de elementos;
- extraccion inicial desde notas de entrevistas;
- clasificacion heuristica por palabras clave;
- nivel de confianza por elemento;
- fuente del elemento: humano o extractor heuristico;
- avance automatico del caso a `as_is_drafting`;
- UI para extraer desde entrevistas, registrar manualmente y revisar inventario;
- pruebas automatizadas de extraccion y captura manual.

## Endpoints nuevos

```text
GET  /api/process-cases/{case_id}/discovery/as-is-elements
POST /api/process-cases/{case_id}/discovery/as-is-elements
POST /api/process-cases/{case_id}/discovery/interviews/{interview_id}/extract-as-is
```

## Tipos de elemento

```text
activity
role
event
business_rule
system
input_output
exception
pain_point
opportunity
metric
control
```

## Extraccion inicial

La extraccion actual es heuristica. Revisa el texto de:

- objetivo de entrevista;
- preguntas;
- notas;
- resumen.

Luego divide el texto en fragmentos y clasifica cada uno por senales simples. Ejemplos:

- `inicia`, `termina`, `disparador` -> evento;
- `SAP`, `correo`, `sistema`, `Excel` -> sistema;
- `si`, `debe`, `requiere` -> regla de negocio;
- `falta`, `devuelve`, `error` -> excepcion;
- `demora`, `manual`, `reproceso` -> dolor;
- `automatizar`, `mejorar`, `simplificar` -> oportunidad.

Esta logica no reemplaza al especialista BPM. Su valor es acelerar la primera estructuracion y dejar una base editable.

## Relacion con BPMN

Estos elementos seran la materia prima para las siguientes fases:

1. ordenar actividades;
2. identificar eventos de inicio y fin;
3. mapear roles a lanes;
4. transformar reglas en gateways;
5. vincular excepciones a flujos alternos;
6. convertir sistemas y documentos en anotaciones o data objects;
7. generar una narrativa `as-is` validable.

## Criterio de salida

Esta parte queda completa cuando:

1. se puede extraer elementos desde una entrevista;
2. se puede registrar elementos manualmente;
3. se puede listar el inventario `as-is`;
4. cada elemento mantiene fuente y confianza;
5. el caso pasa a `as_is_drafting`;
6. frontend y backend pasan verificaciones.

## Siguiente parte

La siguiente parte recomendada es `Fase 1 Parte 9`: generar una narrativa `as-is` inicial desde el inventario estructurado.

Esa narrativa debe ser versionada como artefacto del repositorio documental y quedar lista para revision humana.
