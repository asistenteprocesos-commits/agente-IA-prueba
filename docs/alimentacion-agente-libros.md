# Alimentacion del agente con libros

## Donde se ingresan

Los libros se cargan desde el frontend en la seccion `Conocimiento`:

```text
http://127.0.0.1:5175
```

Flujo:

1. abrir la aplicacion;
2. ir a `Conocimiento`;
3. seleccionar uno o varios libros en `Archivos`;
4. elegir `Tipo = Libro`;
5. completar `Tema`, por ejemplo `BPM`, `BPMN`, `process mining`, `transformacion digital`;
6. presionar `Cargar fuentes`;
7. revisar que el estado quede `processed`.

## Que pasa internamente

Por cada libro el sistema:

1. guarda el archivo original en `storage/documents`;
2. registra metadata en `knowledge_documents`;
3. extrae texto;
4. divide el texto en fragmentos;
5. guarda los fragmentos en `knowledge_chunks`;
6. deja la fuente lista para la futura busqueda semantica.

## Como aprende el agente

En esta etapa el agente aun no queda entrenado por fine tuning. El camino correcto es:

```text
libros -> texto -> fragmentos -> embeddings -> busqueda semantica -> respuesta con citas
```

Esto se llama RAG. Es mas seguro para este proyecto porque:

- permite usar muchos libros sin reentrenar el modelo;
- mantiene trazabilidad de fuente;
- evita que el agente invente fundamentos sin evidencia;
- permite actualizar libros sin reconstruir todo el LLM;
- facilita supervision humana.

## Que falta para que consulte los libros

Ya existe:

- carga de libros;
- extraccion de texto;
- fragmentacion;
- almacenamiento;
- analisis inicial de biblioteca;
- extraccion de conceptos en espanol;
- esquema operativo para gestionar casos de proceso.

Falta implementar:

- embeddings locales;
- base vectorial, recomendada `Qdrant`;
- endpoint de busqueda semantica;
- prompt del agente que use fragmentos recuperados;
- respuestas con citas obligatorias;
- evaluacion de calidad de respuesta.

## Analizar libros complejos en ingles

Muchos libros tecnicos estaran en ingles, pero el agente debe trabajar en espanol. La estrategia es:

1. conservar el texto original como fuente;
2. extraer conceptos tecnicos en espanol;
3. mantener el extracto original para trazabilidad;
4. generar una metodologia operativa en espanol;
5. responder siempre con evidencia recuperada desde los libros.

En el frontend, despues de cargar libros, se debe presionar:

```text
Analizar biblioteca
```

Eso crea registros en `knowledge_insights`. Cada aprendizaje conserva:

- documento fuente;
- fragmento fuente;
- idioma original;
- tema;
- tipo de conocimiento;
- resumen en espanol;
- nivel de confianza.

## Uso futuro de GPT-5.5

GPT-5.5 no debe usarse para "memorizar" todos los libros en una sola conversacion. Tampoco conviene hacer fine tuning inicial con libros completos.

Uso recomendado:

1. extraer conceptos de cada fragmento;
2. traducir y normalizar conocimiento tecnico al espanol;
3. construir playbooks de gestion de casos;
4. recuperar fragmentos relevantes por RAG;
5. pedirle al modelo que razone solo con esas fuentes;
6. guardar citas y evidencia.

Cuando exista `OPENAI_API_KEY`, se puede conectar GPT-5.5 como analizador avanzado de fragmentos. Mientras tanto, el proyecto deja una primera capa heuristica para ordenar la biblioteca y probar el flujo.

## Recomendacion de carga inicial

Para los mas de 30 libros:

1. cargar primero 3 a 5 libros clave;
2. revisar que todos queden `processed`;
3. validar fragmentos desde la UI;
4. luego cargar el resto por grupos de 5 a 10 archivos;
5. clasificar por tema para facilitar busqueda futura.

Temas sugeridos:

```text
BPM
BPMN
process mining
lean
six sigma
transformacion digital
automatizacion
gestion del cambio
arquitectura empresarial
riesgos y controles
simulacion de procesos
```

## Nota legal y operativa

Se deben cargar libros y documentos sobre los que tengas permiso de uso dentro del proyecto. El sistema guarda copias locales y fragmentos de texto para consulta interna del agente.
