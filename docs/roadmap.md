# Roadmap del proyecto

## Enfoque

Este proyecto debe avanzar por etapas controladas. La meta no es crear una demo rapida, sino construir una plataforma grande, modular y auditable para gestion de procesos, BPMN y transformacion digital.

La regla principal sera esta: cada etapa debe terminar con un entregable usable, verificable y conectado con la arquitectura general.

## Estado actual v1.1 - 2026-05-13

La base documental y cognitiva del agente ya existe: glosario extendido, patrones BPMN, antipatrones, casos, rubrica, dataset inicial, vault Obsidian, endpoints de perfil de entrenamiento y perfil LLM local.

La brecha principal ya no es conceptual, sino de ejecucion autonoma. El analisis de arquitectura marca que la autonomia completa todavia es baja porque faltan orquestador, agentes especializados, busqueda vectorial real, modelado BPMN automatico, process mining, simulacion y centro de supervision.

Por eso el siguiente bloque no debe volver a Etapa 0. Debe convertir la base de conocimiento v1.1 en capacidades ejecutables v1.2.

## Etapa 0 - Fundacion del producto

Objetivo: dejar claro que vamos a construir, para quien, con que alcance y bajo que reglas de supervision.

Entregables:

- vision del producto;
- alcance funcional inicial;
- usuarios y roles;
- flujo principal del caso de proceso;
- definicion de checkpoints humanos;
- alcance del repositorio documental y versionado;
- riesgos principales;
- backlog inicial;
- criterios para el MVP.

Criterio de salida:

- existe una definicion clara del MVP;
- sabemos que se construye primero y que se deja para despues;
- no hay dudas grandes sobre privacidad, supervision y alcance.

## Etapa 1 - Esqueleto tecnico del MVP

Objetivo: crear una base tecnica ejecutable con backend, frontend, almacenamiento y estructura de modulos.

Entregables:

- backend `FastAPI`;
- frontend `React + TypeScript`;
- configuracion base;
- API de salud;
- estructura de dominios;
- base para autenticacion;
- persistencia inicial;
- repositorio documental inicial por caso;
- aprobaciones documentales;
- historial de versiones;
- comparacion de versiones;
- evidencias vinculadas;
- calidad documental inicial;
- ingestion documental base;
- extraccion de texto y fragmentacion inicial;
- stakeholders del proceso;
- entrevistas y guia inicial de levantamiento `as-is`;
- extraccion inicial de elementos `as-is` desde notas;
- contenedores o scripts de ejecucion local.

Criterio de salida:

- el proyecto levanta localmente;
- frontend y backend se comunican;
- existe una estructura limpia para crecer.

## Etapa 2 - Base de conocimiento documental

Objetivo: permitir cargar libros, documentos internos y evidencias para convertirlos en conocimiento consultable.

Entregables:

- carga de documentos;
- extraccion de texto;
- particion semantica;
- metadatos por fuente;
- embeddings;
- busqueda semantica;
- respuestas con citas.

Criterio de salida:

- se puede cargar un documento;
- se puede consultarlo;
- toda respuesta muestra fuente o evidencia.

## Etapa 2.5 - Repositorio documental de procesos

Objetivo: almacenar y versionar los procesos disenados, tanto flujos BPMN como texto asociado.

Entregables:

- repositorio por caso de proceso;
- artefactos versionados;
- estados documentales;
- historial de cambios;
- aprobaciones por version;
- comparacion basica de versiones;
- busqueda por proceso, actividad, etiqueta y fuente.

Criterio de salida:

- se puede guardar una narrativa;
- se puede guardar un BPMN;
- se puede versionar y aprobar un artefacto;
- una version aprobada no puede ser sobrescrita.

## Etapa 3 - Levantamiento `as-is`

Objetivo: que el sistema ayude a levantar informacion de procesos con areas usuarias.

Entregables:

- gestion de casos de proceso;
- registro de stakeholders;
- cuestionarios guiados;
- plantilla de entrevista;
- captura de notas o transcripciones;
- extraccion de actividades, roles, eventos, reglas, sistemas, entradas, salidas y excepciones;
- generacion de narrativa `as-is`.

Criterio de salida:

- se puede crear un caso;
- el agente puede preparar entrevistas;
- el usuario puede validar una narrativa `as-is`.

## Etapa 3.5 - Process mining inicial

Objetivo: complementar el levantamiento manual con datos reales de ejecucion.

Entregables:

- carga de event logs en CSV;
- mapeo de columnas;
- validacion de calidad del log;
- analisis de variantes;
- analisis de performance;
- descubrimiento inicial del proceso;
- comparacion contra narrativa `as-is`;
- hallazgos trazables basados en datos.

Criterio de salida:

- se puede importar un log;
- se pueden ver variantes principales;
- se pueden detectar desviaciones frente al proceso declarado.

## Etapa 4 - Modelado BPMN `as-is`

Objetivo: convertir informacion estructurada en un modelo BPMN revisable.

Entregables:

- generador BPMN XML;
- editor visual con `bpmn-js`;
- validaciones basicas de consistencia;
- versionado del modelo;
- comentarios y evidencias por actividad;
- aprobacion humana del `as-is`.

Criterio de salida:

- se puede generar un BPMN inicial;
- se puede editar;
- se puede aprobar o rechazar.

## Etapa 5 - Analisis de mejora

Objetivo: identificar problemas, oportunidades, controles faltantes y potenciales automatizaciones.

Entregables:

- matriz de hallazgos;
- clasificacion de desperdicios;
- analisis de riesgos;
- analisis de madurez digital;
- oportunidades de automatizacion;
- trazabilidad entre hallazgo, evidencia y parte del proceso.

Criterio de salida:

- cada recomendacion tiene fuente, impacto estimado y nivel de confianza.

## Etapa 6 - Diseno `to-be`

Objetivo: construir alternativas de proceso futuro junto con las areas involucradas.

Entregables:

- propuestas de `to-be`;
- comparador `as-is` vs `to-be`;
- cambios por rol, sistema, control y regla;
- BPMN `to-be`;
- aprobacion por responsables.

Criterio de salida:

- existe una version `to-be` validada y lista para simulacion.

## Etapa 7 - Simulacion y analisis cuantitativo

Objetivo: estimar impacto operativo antes de presentar el modelo final.

Entregables:

- parametros de simulacion;
- supuestos versionados;
- simulacion discreta;
- escenarios comparativos;
- indicadores de tiempo, capacidad, colas, costo y SLA;
- analisis de sensibilidad.

Criterio de salida:

- se puede justificar la recomendacion con datos y supuestos visibles.

## Etapa 8 - Entregables finales

Objetivo: producir resultados profesionales para decision ejecutiva y ejecucion tecnica.

Entregables:

- informe ejecutivo;
- informe tecnico;
- BPMN XML;
- tablero de resultados;
- presentacion final;
- lista de iniciativas de implementacion;
- matriz de riesgos y controles.

Criterio de salida:

- el caso de proceso queda cerrado con aprobacion humana y entregables exportables.

## Etapa 9 - Autonomia avanzada

Objetivo: convertir el sistema en una plataforma que mejore con cada proyecto.

Entregables:

- memoria organizacional;
- biblioteca de patrones;
- evaluaciones automaticas de calidad;
- observabilidad completa;
- motor de aprendizaje por retroalimentacion;
- agentes especializados por dominio.

Criterio de salida:

- el sistema reutiliza conocimiento de casos anteriores sin perder trazabilidad ni control humano.

## Orden inmediato

La `Etapa 0` y la base de `Etapa 1` ya estan documentadas. El orden inmediato para retomar es `v1.2`:

1. `RAG vectorial`: embeddings + indice local/vectorial + busqueda semantica con citas.
2. `Orquestador minimo`: maquina de estados para fases del caso, con checkpoints humanos. Estado: implementado como Fase 1.B inicial.
3. `Agente Levantador`: preguntas por rol, vacios, contradicciones y completitud. Estado: implementado inicial.
4. `Agente Modelador BPMN`: generar BPMN XML inicial y validarlo. Estado: implementado inicial.
5. `Agente Analista`: hallazgos, cuellos, riesgos, controles y metricas. Estado: implementado inicial.
6. `Agente Redisenador`: alternativas to-be, impacto, esfuerzo y riesgo. Estado: implementado inicial.
7. `Agente Simulador`: escenarios, sensibilidad y resultados cuantitativos. Estado: implementado inicial.
8. `Agente Redactor`: informe ejecutivo, tecnico y plan de implementacion. Estado: implementado inicial.
9. `Agente Supervisor avanzado`: aprobaciones, bloqueos y escalamiento.
10. `Pruebas de conocimiento`: preguntas reales BPM respondidas con fuentes, score y brechas.
11. `Validador BPMN`: cargar XML BPMN y detectar errores basicos contra patrones.
12. `Process mining inicial`: carga de CSV, mapeo de columnas y primeras variantes.

El MVP inicial se mantiene como un MVP combinado pero pequeno:

1. `MVP documental`: cargar libros y consultar conocimiento BPM con citas.
2. `MVP de levantamiento`: crear casos, entrevistar y producir narrativa `as-is`.
3. `MVP BPMN`: generar y editar BPMN desde una narrativa de proceso.
4. `MVP process mining`: cargar event logs y contrastarlos contra el `as-is`.

Recomendacion practica:

- cargar documentos;
- crear un caso de proceso;
- registrar stakeholders;
- generar cuestionario;
- capturar narrativa `as-is`;
- cargar un event log simple si existe;
- generar un BPMN inicial simple;
- guardar narrativa y BPMN con control de versiones;
- pedir aprobacion humana.

Ese camino prueba el corazon del producto sin intentar simular todo desde el primer dia.
