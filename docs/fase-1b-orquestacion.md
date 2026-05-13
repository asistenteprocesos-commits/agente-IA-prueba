# Fase 1.B - Orquestacion del agente BPM

Fecha: 2026-05-13

## Objetivo

Crear el backbone del agente autonomo para ejecutar el ciclo BPM completo con fases, contexto compartido, checkpoints humanos y rollback.

## Estado implementado

Se implemento una primera version funcional del orquestador:

- modelo persistente `orchestration_runs`;
- modelo de fases `orchestration_phases`;
- bitacora de eventos `orchestration_events`;
- maquina de 8 fases alineada con la arquitectura objetivo;
- checkpoint humano por fase critica;
- aprobacion y rechazo de checkpoint;
- rollback hacia fase previa;
- contexto compartido entre fases;
- panel frontend para ver avance, fases, eventos y bloqueos.

## Fases configuradas

1. Preparar alcance y conocimiento
2. Levantar as-is
3. Estructurar elementos as-is
4. Modelar BPMN as-is
5. Analizar datos y performance
6. Identificar mejoras y riesgos
7. Disenar to-be y simular
8. Cerrar y presentar

## Endpoints

```text
GET  /api/process-cases/{case_id}/orchestration
POST /api/process-cases/{case_id}/orchestration/start
POST /api/process-cases/{case_id}/orchestration/advance
POST /api/process-cases/{case_id}/orchestration/checkpoint
POST /api/process-cases/{case_id}/orchestration/rollback
POST /api/process-cases/{case_id}/orchestration/context
```

## Pendiente de esta fase

- integrar LangGraph o un adaptador equivalente para ejecutar agentes reales por fase;
- conectar cada fase con agentes especializados;
- usar RAG vectorial para decisiones con evidencia;
- agregar politicas de reintento, compensacion y escalamiento;
- generar tareas automaticas del agente levantador.

## Siguiente paso en orden

Construir el `Agente Levantador` sobre este backbone:

- generar cuestionarios por rol;
- detectar vacios de levantamiento;
- detectar contradicciones;
- calcular completitud del as-is;
- proponer siguiente entrevista o taller.
