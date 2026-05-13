# Fase 2.2 - Agente Modelador BPMN

Fecha: 2026-05-13

## Objetivo

Transformar el levantamiento as-is en un primer BPMN XML validable, versionado y listo para revision humana.

## Estado implementado

Se implemento una primera version funcional:

- generacion de BPMN XML as-is desde elementos levantados;
- evento de inicio, tareas, gateways basicos, excepciones y evento de fin;
- validacion basica BPMN 2.0;
- deteccion de XML invalido;
- deteccion de tareas sin nombre;
- validacion de referencias `sourceRef` y `targetRef`;
- advertencias por gateways sin alternativas;
- guardado del BPMN como artefacto versionado en el repositorio;
- panel frontend para generar, guardar y revisar issues.

## Endpoints

```text
GET  /api/process-cases/{case_id}/bpmn/as-is/preview
POST /api/process-cases/{case_id}/bpmn/as-is/generate
POST /api/process-cases/{case_id}/bpmn/validate
```

## Pendiente

- visualizador con `bpmn-js`;
- layout automatico de diagramas;
- modelado avanzado de eventos intermedios, pools, lanes, message flows y subprocesos;
- sugerencias de mejora de notacion;
- validacion BPMN mas estricta con reglas de patrones/antipatrones.

## Siguiente paso en orden

Construir el `Agente Analista`:

- identificar cuellos de botella;
- clasificar desperdicios;
- mapear riesgos y controles;
- calcular metricas iniciales desde elementos y entrevistas;
- preparar base para process mining.
