# Fase 2.4 - Agente Redisenador

Fecha: 2026-05-13

## Objetivo

Generar alternativas `to-be` a partir del analisis as-is, separando quick wins, cambios estructurales, controles y automatizaciones.

## Estado implementado

Se implemento una primera version funcional:

- alternativas to-be desde hallazgos del Agente Analista;
- quick wins para validacion temprana;
- alternativas estructurales para colas y SLA;
- alternativas de automatizacion para handoffs manuales;
- alternativas de control por excepcion;
- comparacion con opcion recomendada;
- supuestos y validaciones requeridas;
- guardado de propuesta to-be como artefacto versionado;
- panel frontend de alternativas to-be.

## Endpoints

```text
GET  /api/process-cases/{case_id}/redesign/to-be-options
POST /api/process-cases/{case_id}/redesign/report
```

## Pendiente

- estimacion cuantitativa por alternativa;
- workshop asistido con areas involucradas;
- versionado comparativo de multiples to-be;
- generacion de BPMN to-be;
- conexion con motor de simulacion.

## Siguiente paso en orden

Construir el `Agente Simulador`:

- parametros de simulacion;
- escenarios as-is vs to-be;
- sensibilidad de tiempo, capacidad y costo;
- resultados versionados.
