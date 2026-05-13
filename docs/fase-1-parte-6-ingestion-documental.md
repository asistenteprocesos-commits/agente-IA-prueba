# Fase 1 - Parte 6 - Ingestion documental

## Objetivo

Crear la primera entrada real para alimentar al agente con libros, guias, normas, documentos internos y evidencias tecnicas.

Esta parte no implementa todavia RAG completo ni entrenamiento de modelos. Su funcion es dejar preparada la biblioteca documental: guardar el archivo original, extraer texto, dividirlo en fragmentos y mantener metadata trazable.

## Incluido

- carga de archivos desde el frontend;
- carga multiple de libros y documentos;
- almacenamiento fisico en `storage/documents`;
- tabla de documentos fuente;
- tabla de fragmentos de texto;
- metadata por documento: titulo, autor, tipo, tema, idioma y caso asociado;
- extraccion de texto para `.txt`, `.md`, `.csv`, `.json`, `.xml`, `.bpmn`, `.pdf` y `.docx`;
- fragmentacion inicial por tamano y puntos naturales de corte;
- consulta de documentos cargados;
- consulta de fragmentos por documento;
- prueba automatizada de ingesta de texto.

## Endpoints nuevos

```text
GET  /api/knowledge/documents
POST /api/knowledge/documents
POST /api/knowledge/documents/bulk
GET  /api/knowledge/documents/{document_id}/chunks
```

El `POST /documents` usa `multipart/form-data` con:

```text
file
title
author
source_type
subject_area
language
case_id
```

El `POST /documents/bulk` usa:

```text
files
author
source_type
subject_area
language
case_id
```

## Donde ingresar los libros

En el frontend:

```text
http://127.0.0.1:5175
```

Se debe usar la seccion `Conocimiento`:

1. seleccionar varios archivos en el campo `Archivos`;
2. dejar `Tipo` como `Libro`;
3. completar `Autor` si aplica a todos los archivos seleccionados;
4. completar `Tema`, por ejemplo `BPMN`, `BPM`, `process mining` o `transformacion digital`;
5. mantener `Idioma` como `es` o cambiarlo segun el material;
6. presionar `Cargar fuentes`.

Los formatos soportados son:

```text
.txt
.md
.csv
.json
.xml
.bpmn
.pdf
.docx
```

Los archivos originales quedan en:

```text
storage/documents
```

El texto procesado queda en base de datos, dividido en fragmentos en `knowledge_chunks`.

## Tipos de fuente

```text
book
article
internal_document
standard
interview
process_artifact
other
```

## Relacion con machine learning

La Parte 6 prepara los datos, pero aun no entrena ni ajusta un modelo.

Para este proyecto, "alimentar al agente con libros" no significa modificar el LLM directamente desde el primer dia. La opcion correcta para empezar es RAG: el agente consulta fragmentos de los libros cuando analiza procesos, y responde usando esas fuentes como evidencia.

La estrategia recomendada para las siguientes fases es:

1. mantener los libros como fuentes versionadas y trazables;
2. generar embeddings de cada fragmento;
3. guardar vectores en una base vectorial local, por ejemplo `Qdrant`;
4. usar busqueda semantica para recuperar fragmentos relevantes;
5. pasar esos fragmentos al LLM gratuito/local como contexto;
6. exigir citas y evidencia en cada respuesta del agente.

Esto permite alimentar al agente con mas de 30 libros sin hacer fine tuning inicial. El fine tuning solo deberia evaluarse despues, cuando exista un conjunto propio de ejemplos validados por especialistas.

## Criterio de salida

Esta parte queda completa cuando:

1. se puede cargar un documento;
2. se extrae texto;
3. se generan fragmentos;
4. se listan documentos desde la API;
5. se consultan fragmentos desde la API;
6. el frontend permite cargar y revisar fuentes;
7. las pruebas de backend y el build de frontend pasan.

## Siguiente parte

La `Fase 1 Parte 7` prepara el esquema de stakeholders y entrevistas para levantamiento `as-is`.

Luego, en `Fase 2`, se debe conectar esta biblioteca con:

- embeddings locales;
- busqueda semantica;
- respuestas con citas;
- ranking de fuentes;
- control de calidad de respuestas;
- supervision humana para conocimiento sensible.
