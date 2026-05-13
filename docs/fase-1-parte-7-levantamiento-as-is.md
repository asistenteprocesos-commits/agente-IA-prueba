# Fase 1 - Parte 7 - Levantamiento as-is

## Objetivo

Agregar la base operativa para levantar informacion del proceso actual con las areas involucradas.

Esta parte permite registrar stakeholders, planificar entrevistas y usar una guia inicial de preguntas para obtener informacion `as-is` antes de modelar BPMN.

## Incluido

- registro de participantes por caso;
- clasificacion de rol e influencia;
- disponibilidad y notas por stakeholder;
- registro de entrevistas, talleres, observaciones y seguimientos;
- estado de la entrevista: planificada, agendada, completada o cancelada;
- preguntas, notas y resumen por sesion;
- guia inicial de levantamiento `as-is`;
- cambio automatico del caso a estado `discovery` cuando inicia el levantamiento;
- UI para gestionar participantes, entrevistas y guia;
- pruebas automatizadas de stakeholders, entrevistas y guia.

## Endpoints nuevos

```text
GET  /api/process-cases/{case_id}/discovery/stakeholders
POST /api/process-cases/{case_id}/discovery/stakeholders
GET  /api/process-cases/{case_id}/discovery/interviews
POST /api/process-cases/{case_id}/discovery/interviews
GET  /api/process-cases/{case_id}/discovery/interview-guide
```

## Roles de stakeholder

```text
process_owner
subject_matter_expert
approver
participant
system_owner
risk_control
external
```

## Tipos de entrevista

```text
discovery
validation
workshop
observation
follow_up
```

## Guia inicial

La guia se genera por caso y cubre:

- contexto y alcance;
- flujo actual;
- roles, sistemas y datos;
- medicion y mejora.

Esta guia es una primera version. Mas adelante el agente debe adaptarla segun el tipo de proceso, los documentos cargados, hallazgos previos y riesgos del dominio.

## Criterio de salida

Esta parte queda completa cuando:

1. se puede registrar un stakeholder;
2. se puede registrar una entrevista vinculada;
3. se puede listar stakeholders y entrevistas;
4. se genera una guia de levantamiento `as-is`;
5. el caso pasa a `discovery` al iniciar el levantamiento;
6. frontend y backend pasan verificaciones.

## Siguiente parte

La `Fase 1 Parte 8` extrae elementos `as-is` desde notas de entrevistas.

Ese paso empieza a estructurar:

- actividades;
- roles;
- eventos;
- reglas de negocio;
- sistemas;
- entradas y salidas;
- excepciones;
- problemas y oportunidades.
