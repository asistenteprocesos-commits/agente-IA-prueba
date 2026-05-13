# Fase 2.5 - Agente Simulador

Fecha: 2026-05-13

## Objetivo

Comparar escenarios as-is y to-be con supuestos visibles antes de aprobar una recomendacion.

## Estado implementado

Se implemento una primera version funcional:

- escenario as-is base;
- escenarios por alternativa to-be;
- reduccion estimada de tiempo de ciclo;
- esfuerzo manual estimado;
- indice de costo;
- riesgo SLA;
- sensibilidad basica por volumen, aprobacion y reproceso;
- guardado de resultado como artefacto versionado;
- panel frontend de simulacion.

## Endpoints

```text
GET  /api/process-cases/{case_id}/simulation/scenarios
POST /api/process-cases/{case_id}/simulation/report
```

## Pendiente

- integracion con SimPy o PM4Py;
- simulacion discreta con recursos, colas y distribuciones;
- calibracion con event logs;
- comparacion de multiples versiones to-be;
- analisis de sensibilidad parametrico.

## Siguiente paso en orden

Construir el `Agente Redactor`:

- informe ejecutivo;
- informe tecnico;
- plan de implementacion;
- matriz final de riesgos y controles;
- entregables versionados.
