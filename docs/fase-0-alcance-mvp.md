# Fase 0 - Alcance del MVP

## Objetivo del MVP

Construir una primera version funcional que pruebe el ciclo principal del producto:

```text
caso -> documentos -> stakeholders -> entrevista -> event log opcional -> hechos -> narrativa -> BPMN -> repositorio versionado -> aprobacion
```

El MVP debe demostrar que el agente puede trabajar con conocimiento, levantar informacion, producir un `as-is`, generar un BPMN inicial y guardar todo con versionado y supervision humana.

## Alcance incluido

### 1. Gestion de casos

- crear caso de proceso;
- definir nombre, area, objetivo, alcance y estado;
- registrar responsable;
- ver tablero simple de casos.

### 2. Gestion documental

- cargar documentos fuente;
- guardar artefactos generados;
- versionar narrativas y BPMN;
- consultar historial de versiones;
- enlazar evidencias a artefactos;
- mantener estados documentales.

### 3. Base de conocimiento

- procesar documentos;
- dividir contenido en fragmentos;
- guardar metadata basica;
- consultar con busqueda semantica;
- responder con citas.

### 4. Levantamiento `as-is`

- registrar stakeholders;
- generar cuestionario inicial por rol;
- capturar notas manuales de entrevista;
- extraer hechos del proceso;
- generar narrativa `as-is`;
- pedir validacion humana.

### 5. Process mining opcional

- cargar CSV de event log;
- mapear columnas minimas;
- validar calidad basica;
- detectar variantes principales;
- generar hallazgos iniciales.

### 6. BPMN inicial

- generar BPMN XML simple desde la narrativa;
- visualizar el diagrama;
- guardar version;
- solicitar aprobacion.

### 7. Supervision humana

- crear tareas de revision;
- aprobar o rechazar narrativa;
- aprobar o rechazar BPMN;
- registrar comentarios y decisiones.

## Fuera de alcance para el MVP

- simulacion avanzada;
- integraciones con calendarios;
- entrevistas automaticas por videollamada;
- conectores nativos ERP/CRM;
- SSO empresarial;
- permisos avanzados por organizacion;
- exportacion profesional completa a Word, PDF y PowerPoint;
- motor avanzado de comparacion visual BPMN;
- aprendizaje entre clientes.

## Criterios de aceptacion

El MVP sera aceptable cuando:

1. se pueda crear un caso de proceso;
2. se puedan cargar documentos;
3. el agente pueda responder usando fuentes;
4. se puedan registrar stakeholders;
5. se pueda generar un cuestionario;
6. se pueda capturar una entrevista manual;
7. se pueda generar una narrativa `as-is`;
8. se pueda guardar una version de la narrativa;
9. se pueda generar y guardar un BPMN inicial;
10. se pueda aprobar o rechazar el BPMN;
11. el repositorio muestre historial de artefactos;
12. cada salida importante tenga evidencia o decision asociada.

## Supuestos iniciales

- el MVP sera web y local primero;
- tendra una sola organizacion;
- usara usuarios simples al inicio;
- el almacenamiento de archivos puede empezar en filesystem local y migrar a MinIO;
- `PostgreSQL` sera la fuente principal de metadata;
- `Qdrant` sera el almacen vectorial;
- `PM4Py` sera el motor inicial de process mining;
- `Gemini 2.5 Flash-Lite` sera el LLM principal de arranque;
- `Ollama` quedara preparado como proveedor local.

## Resultado esperado

Al final del MVP tendremos una plataforma pequena pero real, capaz de demostrar el ciclo completo del producto sin depender de funciones decorativas.
