# ADR 003 - Gestion documental y versionado de procesos

## Estado

Propuesto

## Fecha

2026-05-12

## Decision

Incluir un modulo formal de `Gestion documental y repositorio de procesos` para almacenar, versionar, consultar y auditar todos los artefactos generados durante el ciclo de vida de un proceso.

Este modulo debe guardar tanto los flujos como el texto asociado:

- BPMN XML;
- diagramas renderizados;
- narrativa `as-is`;
- narrativa `to-be`;
- reglas de negocio;
- supuestos;
- hallazgos;
- evidencias;
- resultados de process mining;
- parametros de simulacion;
- informes y entregables finales.

## Contexto

El producto no solo va a analizar procesos. Tambien debe convertirse en el repositorio controlado donde vive la historia del proceso.

Un proceso disenado no es solo un diagrama. Es un paquete de conocimiento compuesto por:

- modelo BPMN;
- descripcion textual;
- responsables;
- entradas y salidas;
- sistemas;
- reglas;
- controles;
- riesgos;
- versiones;
- aprobaciones;
- evidencia que justifica cada cambio.

Si esto no se controla desde el inicio, el sistema podria generar buenos modelos pero perder trazabilidad, comparabilidad y gobierno.

## Enfoque tecnico

Usar una estrategia mixta:

- `PostgreSQL` para metadata, versiones, estados, aprobaciones, relaciones y auditoria.
- `MinIO` o filesystem gestionado para archivos binarios y artefactos pesados.
- `Qdrant` para busqueda semantica sobre contenido textual.
- versionado de dominio dentro de la aplicacion, no depender solo de Git.

Git puede usarse despues como exportacion tecnica opcional, pero no debe ser el sistema principal de versionado funcional para usuarios de negocio.

## Artefactos controlados

Tipos iniciales:

- `process_narrative_as_is`
- `process_narrative_to_be`
- `bpmn_xml_as_is`
- `bpmn_xml_to_be`
- `bpmn_diagram_svg`
- `bpmn_diagram_png`
- `interview_notes`
- `transcript`
- `event_log`
- `mining_report`
- `simulation_parameters`
- `simulation_result`
- `improvement_report`
- `final_report`
- `presentation`

## Versionado

Cada artefacto debe tener versiones inmutables.

Formato recomendado:

```text
major.minor.patch
```

Reglas:

- `major`: version aprobada formalmente o cambio estructural relevante.
- `minor`: cambio funcional revisable.
- `patch`: ajuste menor, correccion o autosave consolidado.

Cada version debe registrar:

- autor;
- fecha;
- origen del cambio;
- motivo;
- resumen;
- version anterior;
- estado;
- aprobacion asociada;
- hash del contenido;
- referencias a evidencias.

## Estados documentales

Estados iniciales:

```text
draft
in_review
changes_requested
approved
published
superseded
archived
rejected
```

## Capacidades requeridas

1. crear repositorio por caso de proceso;
2. guardar artefactos por tipo;
3. versionar BPMN y texto;
4. comparar versiones;
5. registrar aprobaciones;
6. bloquear edicion de versiones aprobadas;
7. crear nueva version desde una aprobada;
8. buscar por texto, proceso, rol, sistema, actividad o etiqueta;
9. enlazar evidencias a actividades BPMN;
10. exportar paquete documental completo.

## Relacion con BPMN

El BPMN XML debe ser tratado como artefacto principal versionado.

Cada tarea, gateway, evento o flujo relevante debe poder enlazarse a:

- hechos extraidos de entrevistas;
- fragmentos documentales;
- hallazgos de process mining;
- supuestos;
- controles;
- riesgos;
- decisiones humanas.

## Relacion con IA

Los agentes pueden crear borradores, comparaciones y propuestas, pero no deben sobrescribir versiones aprobadas.

Reglas:

- todo cambio generado por IA queda como borrador;
- toda publicacion requiere aprobacion humana;
- las respuestas del agente deben citar artefactos y versiones;
- las recomendaciones deben indicar version de BPMN y narrativa usada.

## Modelo de datos adicional

Entidades nuevas:

- `ProcessRepository`
- `ProcessArtifact`
- `ArtifactVersion`
- `ArtifactRelation`
- `VersionDiff`
- `DocumentApproval`
- `DocumentTag`
- `ArtifactComment`
- `PublishedProcessPackage`

## Riesgos

1. `Versiones ambiguas`: se mitiga con estados, hashes y version anterior obligatoria.
2. `BPMN y narrativa desalineados`: se mitiga enlazando versiones y validando consistencia antes de aprobar.
3. `Sobrescritura accidental`: se mitiga con artefactos inmutables una vez aprobados.
4. `Archivos sin contexto`: se mitiga con metadata obligatoria.
5. `Busqueda sin trazabilidad`: se mitiga devolviendo artefacto, version y fuente.

## Decision de implementacion

Crear un modulo `process_repository` en el backend.

Responsabilidades iniciales:

- crear repositorio por caso;
- guardar artefactos y versiones;
- controlar estados documentales;
- comparar versiones de texto;
- registrar metadata de BPMN;
- asociar aprobaciones;
- exponer API para consultar historial.

Este modulo debe existir desde el MVP, aunque sus capacidades avanzadas se completen por etapas.
