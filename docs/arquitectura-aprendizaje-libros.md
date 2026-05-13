# Arquitectura de aprendizaje desde libros

## Problema

El agente debe trabajar con muchos libros tecnicos, varios en ingles, sobre BPM, BPMN, process mining, transformacion digital, riesgos, controles, simulacion y mejora continua.

El objetivo no es que el modelo "recuerde" todo de forma opaca. El objetivo es que el sistema convierta esos libros en conocimiento consultable, trazable y aplicable a cada caso de proceso.

## Decision

Usar una arquitectura de aprendizaje documental por capas:

```text
Libros originales
  -> extraccion de texto
  -> fragmentos
  -> aprendizajes estructurados en espanol
  -> embeddings y busqueda semantica
  -> razonamiento del agente con citas
  -> metodologia de gestion de casos
```

## Por que no fine tuning ahora

No se recomienda iniciar con fine tuning porque:

- los libros completos pueden superar limites y restricciones practicas;
- el conocimiento debe conservar citas;
- el contenido puede cambiar o ampliarse;
- el fine tuning no garantiza memoria exacta;
- el agente necesita justificar recomendaciones con fuentes;
- antes se requieren ejemplos propios validados por especialistas.

Fine tuning podria evaluarse despues para estilos de respuesta o patrones repetitivos, no como repositorio principal de conocimiento.

## Rol de GPT-5.5

GPT-5.5 puede usarse como motor avanzado para:

- extraer conceptos desde fragmentos complejos;
- traducir conocimiento tecnico del ingles al espanol;
- sintetizar marcos de trabajo;
- comparar autores;
- construir checklists por fase;
- razonar sobre casos usando fragmentos recuperados;
- redactar entregables profesionales.

Pero GPT-5.5 debe recibir contexto recuperado desde la biblioteca. No debe inventar fuentes ni operar sin citas.

## Estado actual implementado

Ya existe:

- carga multiple de libros;
- extraccion de texto;
- fragmentacion;
- `knowledge_documents`;
- `knowledge_chunks`;
- `knowledge_insights`;
- analisis inicial de biblioteca;
- generacion de esquema operativo de gestion de casos.

Endpoints principales:

```text
POST /api/knowledge/documents/bulk
POST /api/knowledge/learning/analyze
GET  /api/knowledge/insights
GET  /api/knowledge/case-methodology
```

## Siguiente evolucion

La siguiente capa debe agregar:

1. embeddings por fragmento;
2. base vectorial `Qdrant`;
3. busqueda semantica;
4. recuperacion por tema, caso y fase;
5. prompts de agente con citas obligatorias;
6. evaluacion automatica de calidad y trazabilidad.

## Esquema operativo esperado

El agente debe usar la biblioteca para guiar cada caso en fases:

1. preparar alcance y conocimiento;
2. levantar `as-is`;
3. estructurar elementos `as-is`;
4. modelar BPMN `as-is`;
5. analizar datos y performance;
6. identificar mejoras y riesgos;
7. disenar `to-be` y simular;
8. cerrar y gobernar entregables.

Cada fase debe estar soportada por conceptos, reglas y evidencia derivados de los libros.
