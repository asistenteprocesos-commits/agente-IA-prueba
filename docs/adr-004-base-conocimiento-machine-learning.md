# ADR 004 - Base de conocimiento y machine learning

## Estado

Propuesto

## Fecha

2026-05-12

## Decision

La alimentacion del agente con libros, documentos y conocimiento experto se hara mediante un modulo formal de `Base de conocimiento y machine learning`.

Este modulo no sera una carpeta de PDFs. Sera un pipeline completo:

```text
libros/documentos -> extraccion -> limpieza -> fragmentacion -> metadata -> embeddings -> Qdrant -> RAG -> agentes
```

## Donde vive en la arquitectura

El conocimiento vive en el modulo `Base de conocimiento BPM y transformacion`.

Se conecta con:

- `Repositorio documental`: para almacenar libros, documentos fuente y artefactos generados;
- `Qdrant`: para busqueda semantica;
- `PostgreSQL`: para metadata, autores, temas, permisos, versiones y trazabilidad;
- `Orquestador de agentes`: para responder, razonar y citar fuentes;
- `Motor BPMN`: para reglas, patrones y buenas practicas;
- `Motor analitico`: para marcos de mejora, riesgos, madurez digital y automatizacion.

## Tipos de informacion a cargar

### Conocimiento experto

- libros BPM;
- libros BPMN;
- libros de transformacion digital;
- libros de mejora continua;
- marcos Lean, Six Sigma, TOC y calidad;
- manuales internos;
- politicas;
- procedimientos;
- taxonomias y glosarios.

### Conocimiento de procesos

- narrativas `as-is`;
- narrativas `to-be`;
- BPMN XML;
- entrevistas;
- transcripciones;
- hallazgos;
- simulaciones;
- resultados de process mining;
- decisiones y aprobaciones.

## Machine learning incluido desde el inicio

Para el MVP, machine learning no significa entrenar un LLM desde cero. Significa usar modelos y tecnicas ML para recuperar, clasificar, comparar y evaluar informacion.

Capacidades iniciales:

1. `Embeddings`: convertir fragmentos de libros y documentos en vectores.
2. `Busqueda semantica`: encontrar conocimiento relevante aunque no coincida palabra por palabra.
3. `RAG`: generar respuestas con citas y evidencia.
4. `Clasificacion`: identificar temas como BPMN, control, riesgo, SLA, automatizacion o desperdicio.
5. `Extraccion estructurada`: convertir texto en actividades, roles, reglas, entradas, salidas y eventos.
6. `Clustering`: agrupar documentos, hallazgos o variantes similares.
7. `Scoring`: estimar confianza, calidad de fuente y completitud.

Capacidades futuras:

- reranking semantico;
- deteccion de contradicciones;
- recomendaciones por similitud con casos anteriores;
- modelos predictivos sobre duracion, riesgo o reproceso;
- aprendizaje por retroalimentacion humana;
- fine-tuning solo si la evidencia demuestra que RAG no basta.

## Estrategia para los mas de 30 libros

Cada libro debe entrar con metadata obligatoria:

- titulo;
- autor;
- ano;
- editorial o fuente;
- tema principal;
- subtemas;
- tipo de documento;
- idioma;
- derechos/uso permitido;
- version cargada;
- fecha de ingestion.

Cada fragmento debe registrar:

- libro origen;
- capitulo o seccion;
- pagina si esta disponible;
- texto normalizado;
- embedding;
- etiquetas semanticas;
- nivel de confianza de extraccion.

## Flujo de ingestion

```text
1. Cargar libro o documento
2. Registrar metadata
3. Extraer texto
4. Limpiar y normalizar
5. Dividir en fragmentos semanticos
6. Crear embeddings
7. Guardar fragmentos y vectores
8. Crear indice de busqueda
9. Ejecutar prueba de recuperacion
10. Publicar como fuente disponible para agentes
```

## Reglas de uso por agentes

- ningun agente debe citar un libro si no recupero fragmentos relevantes;
- toda respuesta conceptual debe incluir fuente cuando venga de libros;
- toda recomendacion de proceso debe separar conocimiento experto, evidencia del caso y supuesto;
- los libros alimentan al agente como memoria consultable, no como verdad unica;
- las fuentes aprobadas deben poder desactivarse o versionarse.

## Entidades nuevas

- `KnowledgeSource`
- `KnowledgeDocument`
- `KnowledgeChunk`
- `EmbeddingRecord`
- `RetrievalRun`
- `Citation`
- `KnowledgeTag`
- `KnowledgeEvaluation`

## Relacion con libros y derechos

El sistema debe permitir cargar libros para uso interno autorizado. No debe redistribuir contenido protegido ni producir copias extensas de los libros.

El objetivo tecnico es recuperar fragmentos relevantes y generar sintesis con trazabilidad.

## Decision de implementacion

La primera implementacion se construira en la Fase 2.

La Fase 1 solo deja preparada la arquitectura. La Fase 2 implementara:

- carga de documentos;
- extraccion de texto;
- fragmentacion;
- embeddings;
- Qdrant;
- consulta con citas;
- evaluacion basica de recuperacion.
