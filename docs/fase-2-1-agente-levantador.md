# Fase 2.1 - Agente Levantador

Fecha: 2026-05-13

## Objetivo

Convertir el levantamiento as-is en una capacidad asistida por agente, no solo en captura manual de entrevistas.

## Estado implementado

Se implemento una primera version funcional del Agente Levantador:

- assessment de completitud del levantamiento;
- preguntas inteligentes por rol;
- deteccion de vacios criticos y medios;
- deteccion heuristica de contradicciones;
- recomendaciones de siguiente accion;
- visualizacion en frontend dentro de `Levantamiento`;
- pruebas automatizadas.

## Endpoint

```text
GET /api/process-cases/{case_id}/discovery/assessment
```

## Dimensiones evaluadas

- stakeholders y responsables;
- entrevistas y fuentes;
- flujo, eventos y actividades;
- reglas, sistemas y datos;
- excepciones, metricas y controles;
- trazabilidad y confianza.

## Pendiente

- generar entrevistas completas con LLM local;
- conectar agenda y calendario;
- aceptar transcripciones y resumirlas automaticamente;
- abrir tareas de seguimiento por vacio detectado;
- alimentar el orquestador para bloquear avance si el as-is no esta listo.

## Siguiente paso en orden

Construir el `Agente Modelador BPMN`:

- convertir elementos as-is en BPMN XML inicial;
- validar errores comunes de BPMN 2.0;
- registrar el BPMN como artefacto versionado;
- preparar la base para visualizar con `bpmn-js`.
