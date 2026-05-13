# Fase 0 - Backlog inicial

## Epica 1 - Base tecnica

- crear estructura `backend`;
- crear estructura `frontend`;
- configurar entorno local;
- crear API de salud;
- conectar frontend con backend;
- definir configuracion por variables de entorno.

## Epica 2 - Casos de proceso

- crear entidad `ProcessCase`;
- listar casos;
- ver detalle de caso;
- actualizar estado del caso;
- registrar alcance inicial;
- asociar responsable.

## Epica 3 - Repositorio documental de procesos

- crear repositorio por caso;
- cargar documento o artefacto;
- crear version de artefacto;
- listar artefactos por caso;
- ver historial de versiones;
- bloquear version aprobada;
- registrar comentario de cambio;
- enlazar evidencia con version.

## Epica 4 - Ingestion documental y RAG

- cargar PDF, DOCX, TXT o Markdown;
- extraer texto;
- dividir en fragmentos;
- guardar metadata;
- crear embeddings;
- consultar documentos;
- devolver citas por respuesta.

## Epica 5 - Stakeholders y entrevistas

- crear stakeholder;
- clasificar stakeholder por rol;
- generar cuestionario inicial;
- registrar respuestas o notas;
- extraer hechos del proceso;
- marcar informacion faltante.

## Epica 6 - Narrativa `as-is`

- consolidar hechos;
- generar narrativa estructurada;
- versionar narrativa;
- solicitar revision;
- registrar aprobacion o rechazo.

## Epica 7 - BPMN inicial

- transformar narrativa en estructura de proceso;
- generar BPMN XML basico;
- visualizar BPMN;
- versionar BPMN;
- aprobar o rechazar BPMN.

## Epica 8 - Process mining inicial

- cargar event log CSV;
- mapear columnas;
- validar campos minimos;
- calcular variantes;
- calcular tiempos basicos;
- generar hallazgos preliminares.

## Epica 9 - Supervision humana

- crear tarea de aprobacion;
- asignar revisor;
- registrar decision;
- guardar comentario;
- cambiar estado del caso segun aprobacion.

## Epica 10 - Observabilidad minima

- registrar ejecuciones de agente;
- guardar prompt, modelo y resultado resumido;
- registrar errores;
- registrar fuente de cada recomendacion;
- mostrar historial de acciones del caso.

## Prioridad de construccion

1. Base tecnica.
2. Casos de proceso.
3. Repositorio documental.
4. Ingestion documental.
5. Stakeholders y entrevistas.
6. Narrativa `as-is`.
7. BPMN inicial.
8. Supervision humana.
9. Process mining inicial.
10. Observabilidad minima.

## Primer incremento construible

El primer incremento debe permitir:

- levantar backend y frontend;
- crear un caso;
- crear repositorio del caso;
- guardar una narrativa manual;
- crear una version;
- aprobar o rechazar esa version.

Ese incremento prueba la base de gobierno antes de activar IA pesada.
