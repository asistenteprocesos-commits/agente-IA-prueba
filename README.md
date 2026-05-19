# agente ia prueba

Software de agente IA autonomo para levantamiento, analisis, modelado y rediseno de procesos empresariales con BPMN, simulacion y supervision humana.

## Vision

El sistema debe poder:

1. Ingerir y estructurar conocimiento desde mas de 30 libros y material tecnico de BPM, BPMN y transformacion digital.
2. Levantar procesos `as-is` con las areas involucradas mediante reuniones, entrevistas, cuestionarios guiados y analisis documental.
3. Construir y validar el modelo BPMN del `as-is`.
4. Identificar mejoras, riesgos, cuellos de botella, controles, automatizaciones y oportunidades de transformacion digital.
5. Disenar el `to-be` con las areas responsables.
6. Ejecutar analisis cuantitativos, cualitativos y simulaciones antes de presentar la version final.
7. Operar de forma autonoma, pero con puntos de supervision y aprobacion humana.

## Base inicial del proyecto

La arquitectura inicial y la decision de stack quedaron documentadas aqui:

- [Arquitectura inicial](</c:/Users/Espana/Documents/agente IA prueba/docs/arquitectura-inicial.md>)
- [ADR 001 - Estrategia de LLM](</c:/Users/Espana/Documents/agente IA prueba/docs/adr-001-estrategia-llm.md>)
- [ADR 002 - Estrategia de process mining](</c:/Users/Espana/Documents/agente IA prueba/docs/adr-002-process-mining.md>)
- [ADR 003 - Gestion documental y versionado](</c:/Users/Espana/Documents/agente IA prueba/docs/adr-003-gestion-documental-versionado.md>)
- [ADR 004 - Base de conocimiento y machine learning](</c:/Users/Espana/Documents/agente IA prueba/docs/adr-004-base-conocimiento-machine-learning.md>)
- [ADR 005 - LLM local gratuito](</c:/Users/Espana/Documents/agente IA prueba/docs/adr-005-llm-local-gratuito.md>)
- [Alimentacion del agente con libros](</c:/Users/Espana/Documents/agente IA prueba/docs/alimentacion-agente-libros.md>)
- [Arquitectura de aprendizaje desde libros](</c:/Users/Espana/Documents/agente IA prueba/docs/arquitectura-aprendizaje-libros.md>)
- [Paquete de entrenamiento documental](</c:/Users/Espana/Documents/agente IA prueba/docs/agent-training/README.md>)
- [Uso del vault Obsidian BPM](</c:/Users/Espana/Documents/agente IA prueba/docs/uso-obsidian-vault.md>)
- [Alcance MVP Fase 0](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-0-alcance-mvp.md>)
- [Backlog Fase 0](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-0-backlog.md>)
- [Decisiones Fase 0](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-0-decisiones.md>)

## Estructura sugerida

```text
agente ia prueba/
  docs/
    arquitectura-inicial.md
    adr-001-estrategia-llm.md
    adr-002-process-mining.md
    adr-003-gestion-documental-versionado.md
    adr-004-base-conocimiento-machine-learning.md
    fase-0-fundacion.md
    fase-0-alcance-mvp.md
    fase-0-backlog.md
    fase-0-decisiones.md
    roadmap.md
```

## Proxima fase recomendada

La `Fase 0` y la base de `Fase 1` ya quedaron documentadas. Segun el analisis v1.1, el proyecto debe retomar en la evolucion `v1.2`:

1. busqueda vectorial con embeddings para consultar libros y evidencias con trazabilidad;
2. validador BPMN automatico y base para generar modelos;
3. feedback loop con rubrica de calidad;
4. orquestador inicial de agentes con estados y checkpoints humanos;
5. process mining inicial sobre event logs CSV.

Los componentes grandes de la `Etapa 1` siguen siendo:

1. `backend` con `FastAPI` y `LangGraph`.
2. `frontend` web con tablero de casos y editor BPMN usando `bpmn-js`.
3. repositorio documental con versionado de narrativas y BPMN.
4. pipeline de ingestion documental.
5. motor de entrevistas y levantamiento `as-is`.
6. motor inicial de process mining con event logs CSV.
7. version 1 del simulador y evaluador de mejoras.

## Ejecutar la base tecnica

Arranque limpio recomendado:

```powershell
.\scripts\start-dev-clean.cmd
```

Backend individual:

```powershell
.\scripts\start-backend.cmd
```

Frontend:

```powershell
.\scripts\start-frontend.cmd
```

Si `.tools` no existe, instala Node.js portable para este proyecto:

```powershell
.\scripts\install-node-portable.cmd
```

URLs locales:

```text
Backend:  http://127.0.0.1:8010/api/health
Docs API: http://127.0.0.1:8010/api/docs
Frontend: http://127.0.0.1:5173
```

## Roadmap

- [Roadmap del proyecto](</c:/Users/Espana/Documents/agente IA prueba/docs/roadmap.md>)
- [Fase 0 - Fundacion](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-0-fundacion.md>)
- [Fase 1 - Parte 1 - Base tecnica](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-1-base-tecnica.md>)
- [Fase 1 - Parte 2 - Casos](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-2-casos.md>)
- [Fase 1 - Parte 3 - Persistencia y repositorio](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-3-persistencia-repositorio.md>)
- [Fase 1 - Parte 4 - Aprobaciones documentales](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-4-aprobaciones-documentales.md>)
- [Fase 1 - Parte 5 - Trazabilidad y calidad](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-5-trazabilidad-calidad.md>)
- [Fase 1 - Parte 6 - Ingestion documental](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-6-ingestion-documental.md>)
- [Fase 1 - Parte 7 - Levantamiento as-is](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-7-levantamiento-as-is.md>)
- [Fase 1 - Parte 8 - Extraccion as-is](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-8-extraccion-as-is.md>)
- [Fase 1 - Parte 9 - Aprendizaje documental](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-9-aprendizaje-documental.md>)
- [Fase 1 - Parte 10 - LLM local y machine learning](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1-parte-10-llm-local-machine-learning.md>)
- [Fase 1.B - Orquestacion](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-1b-orquestacion.md>)
- [Fase 2.1 - Agente Levantador](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-2-1-agente-levantador.md>)
- [Fase 2.2 - Agente Modelador BPMN](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-2-2-agente-modelador-bpmn.md>)
- [Fase 2.3 - Agente Analista](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-2-3-agente-analista.md>)
- [Fase 2.4 - Agente Redisenador](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-2-4-agente-redisenador.md>)
- [Fase 2.5 - Agente Simulador](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-2-5-agente-simulador.md>)
- [Fase 2.6 - Agente Redactor](</c:/Users/Espana/Documents/agente IA prueba/docs/fase-2-6-agente-redactor.md>)

## Memoria documental del agente

Ya existe una primera memoria documental construida con los libros entregados. Esta memoria no modifica los pesos de un LLM: organiza el conocimiento en fragmentos, aprendizajes, metodologia, prompt maestro, dataset y grafo Obsidian.

Endpoint:

```text
GET http://127.0.0.1:8010/api/knowledge/agent-training-profile
```

Vault visual:

```text
storage/obsidian-bpm-vault/BPM_Knowledge_Graph.canvas
```

## LLM local gratuito

El proyecto queda preparado para usar Ollama con modelos gratuitos/locales:

```text
Razonamiento: deepseek-r1:1.5b
Embeddings:   qwen3-embedding:0.6b
```

Tambien se puede usar `deepseek-r1:7b` para analisis mas profundo, pero en esta maquina puede ser lento por la RAM disponible.

Endpoint:

```text
GET http://127.0.0.1:8010/api/local-llm/profile
```

Scripts:

```powershell
.\scripts\install-ollama.cmd
.\scripts\start-ollama.cmd
.\scripts\pull-local-llm-models.cmd
```
dfdf