# Fase 0 - Decisiones iniciales

## Decisiones tomadas

### 1. Producto

El sistema sera una plataforma multiagente para gestion, analisis, modelado y rediseno de procesos, no un chatbot aislado.

### 2. MVP

El MVP probara el ciclo:

```text
caso -> documentos -> entrevista -> narrativa -> BPMN -> versionado -> aprobacion
```

Process mining entrara como modulo opcional desde el diseno, con carga CSV inicial.

### 3. Arquitectura

La arquitectura sera modular:

- `backend`;
- `frontend`;
- `orquestador de agentes`;
- `base de conocimiento`;
- `repositorio documental`;
- `motor BPMN`;
- `motor process mining`;
- `centro de supervision`.

### 4. LLM

La primera estrategia sera hibrida:

- `Gemini 2.5 Flash-Lite` como proveedor principal gratuito;
- `Ollama` con `Gemma 3` o `Qwen3` como alternativa local.

### 5. Process mining

El motor inicial sera `PM4Py`.

### 6. Gestion documental

El proyecto tendra repositorio documental propio con versionado funcional de artefactos. Las versiones aprobadas seran inmutables.

### 7. Almacenamiento

La metadata vivira en `PostgreSQL`.

Los archivos podran iniciar en filesystem local y migrar a `MinIO` sin cambiar el dominio.

### 8. Supervision

Toda salida critica de IA sera borrador hasta que una persona la apruebe.

## Decisiones pendientes

1. Nombre final comercial del producto.
2. Si el primer prototipo tendra login real o usuario unico local.
3. Si se instalara `PostgreSQL` desde el inicio o se usara `SQLite` temporal para acelerar el primer prototipo.
4. Si el frontend iniciara con dashboard completo o pantalla simple de casos.
5. Si el primer BPMN sera generado por IA desde texto o con generador deterministico basado en estructura.

## Recomendaciones para las pendientes

1. Mantener el nombre de proyecto `agente ia prueba` por ahora.
2. Usar usuario unico local en el primer incremento.
3. Usar `PostgreSQL` desde el inicio si queremos evitar migraciones tempranas.
4. Iniciar con pantalla simple de casos y repositorio.
5. Empezar con generador deterministico y luego sumar IA para enriquecer.
