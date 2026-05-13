# Fase 2.3 - Agente Analista

Fecha: 2026-05-13

## Objetivo

Analizar el proceso as-is para identificar hallazgos, cuellos de botella, desperdicios, riesgos, controles, metricas y oportunidades de mejora.

## Estado implementado

Se implemento una primera version funcional:

- deteccion de cuellos de botella desde elementos `pain_point` y texto;
- deteccion de desperdicio por reproceso, devoluciones o informacion faltante;
- deteccion de oportunidades de automatizacion por uso manual, correo o Excel;
- extraccion inicial de metricas numericas desde texto;
- matriz inicial de riesgos y controles;
- candidatos de mejora;
- guardado como reporte versionado;
- panel frontend de analisis.

## Endpoints

```text
GET  /api/process-cases/{case_id}/analysis
POST /api/process-cases/{case_id}/analysis/report
```

## Pendiente

- analizar variantes con process mining;
- calcular tiempos acumulados por flujo;
- integrar event logs;
- estimar impacto con mayor precision;
- enlazar hallazgos a elementos BPMN especificos;
- alimentar automaticamente el Agente Redisenador.

## Siguiente paso en orden

Construir el `Agente Redisenador`:

- generar alternativas to-be;
- comparar impacto, esfuerzo y riesgo;
- proponer quick wins y cambios estructurales;
- preparar insumos para simulacion.
