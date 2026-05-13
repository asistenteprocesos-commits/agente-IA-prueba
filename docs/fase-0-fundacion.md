# Fase 0 - Fundacion del producto

## Objetivo

Definir el alcance inicial del software antes de construir el MVP tecnico.

Esta fase existe para evitar que el proyecto crezca desordenado. Como el producto sera grande, necesitamos una primera version que pruebe el ciclo central:

```text
conocimiento -> levantamiento as-is -> process mining opcional -> BPMN -> repositorio versionado -> supervision humana
```

## Producto objetivo

Una plataforma de IA para especialistas de procesos que permite levantar, analizar, modelar y redisenar procesos empresariales con apoyo de agentes autonomos supervisados.

## Usuarios principales

- `Administrador del sistema`: configura modelos, usuarios, permisos y fuentes de conocimiento.
- `Especialista de procesos`: dirige el levantamiento, valida hallazgos y aprueba modelos.
- `Lider de area`: entrega informacion, valida el proceso `as-is` y revisa el `to-be`.
- `Participante operativo`: responde preguntas y valida actividades especificas.
- `Patrocinador ejecutivo`: revisa impacto, riesgos y recomendacion final.

## MVP recomendado

El primer MVP debe incluir:

- gestion basica de casos de proceso;
- carga de documentos;
- repositorio documental de procesos;
- control de versiones para narrativas y BPMN;
- busqueda semantica con citas;
- registro de stakeholders;
- generacion de cuestionarios por rol;
- captura manual de entrevista o reunion;
- extraccion estructurada del `as-is`;
- carga opcional de event logs CSV;
- analisis inicial de variantes cuando existan datos;
- generacion de BPMN inicial;
- almacenamiento de flujos y textos disenados;
- revision humana y estado de aprobacion.

No debe incluir todavia:

- simulacion avanzada;
- integracion con calendarios;
- automatizacion completa de reuniones;
- exportacion profesional completa;
- control avanzado de permisos;
- memoria organizacional compleja.
- conectores empresariales avanzados de process mining.

## Flujo MVP

```text
1. Crear caso de proceso
2. Cargar documentos relevantes
3. Registrar stakeholders
4. Generar cuestionario por stakeholder
5. Registrar respuestas o notas de entrevista
6. Extraer hechos del proceso
7. Cargar event log si existe
8. Comparar hechos declarados contra datos reales
9. Generar narrativa as-is
10. Generar BPMN inicial
11. Guardar narrativa y BPMN en repositorio versionado
12. Solicitar revision humana
13. Aprobar, rechazar o pedir ajustes
```

## Roles de agentes en el MVP

### Agente documental

Responsable de:

- procesar documentos;
- extraer conceptos;
- responder con citas;
- detectar temas BPM, BPMN y transformacion digital.

### Agente gestor documental

Responsable de:

- guardar artefactos generados;
- crear versiones;
- enlazar evidencias;
- comparar cambios;
- preparar paquetes documentales para revision.

### Agente levantador

Responsable de:

- generar preguntas;
- detectar informacion faltante;
- consolidar entrevistas;
- extraer hechos operativos.

### Agente modelador

Responsable de:

- convertir hechos del proceso en estructura BPMN;
- crear un BPMN inicial;
- detectar inconsistencias basicas.

### Agente de process mining

Responsable de:

- validar event logs;
- identificar variantes;
- detectar tiempos de espera y reprocesos;
- comparar datos reales contra narrativa y BPMN;
- producir hallazgos con evidencia.

### Agente supervisor

Responsable de:

- pausar cuando falte evidencia;
- solicitar aprobacion humana;
- registrar decisiones.

## Primeras entidades del sistema

- `User`
- `Organization`
- `ProcessCase`
- `Stakeholder`
- `Document`
- `DocumentChunk`
- `ProcessRepository`
- `ProcessArtifact`
- `ArtifactVersion`
- `VersionDiff`
- `Interview`
- `EventLog`
- `ProcessEvent`
- `MiningRun`
- `ProcessVariant`
- `ProcessFact`
- `ProcessNarrative`
- `BpmnModel`
- `Approval`
- `AgentRun`

## Primeros estados del caso

```text
draft
knowledge_loading
discovery
event_log_analysis
as_is_drafting
bpmn_drafting
repository_review
human_review
approved_as_is
improvement_analysis
closed
```

## Checkpoints humanos del MVP

1. aprobar alcance del caso;
2. validar hechos extraidos de entrevistas;
3. validar mapeo de event logs si se usa process mining;
4. aprobar narrativa `as-is`;
5. aprobar version documental del BPMN `as-is`;
6. autorizar publicacion de version oficial;
7. autorizar paso a analisis de mejora.

## Riesgos de la Fase 0

- intentar construir demasiadas capacidades antes de tener el ciclo principal funcionando;
- depender de documentos sin buena metadata;
- aceptar respuestas del LLM sin evidencia;
- generar BPMN que parezca correcto pero no represente el proceso real;
- perder trazabilidad entre narrativa, BPMN, evidencia y version aprobada;
- interpretar logs incompletos como si fueran toda la realidad operativa;
- no registrar decisiones humanas.

## Decisiones pendientes

1. Si la primera version sera solo local o tambien web multiusuario.
2. Si usaremos autenticacion desde el inicio o usuarios simples para MVP.
3. Donde se guardaran los libros: filesystem local, MinIO o nube.
4. Que formato BPMN minimo debe soportar la primera version.
5. Que proveedor LLM se conectara primero en codigo.
6. Si el MVP aceptara process mining desde el inicio o quedara como modulo activable despues del primer ciclo.
7. Si el repositorio documental inicia con filesystem local o MinIO.

## Recomendacion para continuar

Construir primero el esqueleto tecnico con backend y frontend. Luego implementar el ciclo minimo:

```text
caso -> documentos -> entrevista -> event log opcional -> hechos -> narrativa -> BPMN -> versionado -> aprobacion
```
