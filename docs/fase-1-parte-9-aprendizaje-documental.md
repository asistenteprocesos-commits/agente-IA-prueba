# Fase 1 - Parte 9 - Aprendizaje documental del agente

## Objetivo

Convertir los libros cargados en memoria operativa para el agente BPM, sin depender todavia de una API externa de GPT-5.5 ni de fine tuning.

Esta parte crea una primera capa de aprendizaje documental:

```text
libros -> texto extraido -> fragmentos -> insights en espanol -> metodologia -> prompt maestro -> dataset -> grafo Obsidian
```

## Alcance implementado

- procesamiento de 2 libros tecnicos de BPM;
- generacion de una metodologia maestra en 8 fases;
- creacion de mas de 5.000 aprendizajes estructurados;
- paquete de entrenamiento documental en `docs/agent-training`;
- dataset JSONL para evaluacion y futuro fine tuning;
- vault Obsidian con notas, temas, fases y canvas visual;
- endpoint de perfil del agente para que el software consulte esta memoria.

## Endpoint nuevo

```text
GET /api/knowledge/agent-training-profile
```

Devuelve:

- modo de entrenamiento documental;
- cantidad de libros procesados;
- paginas procesadas;
- caracteres extraidos;
- aprendizajes generados;
- ejemplos del dataset;
- ruta del vault Obsidian;
- ruta del canvas visual;
- artefactos disponibles;
- siguiente paso recomendado.

## Paquete de entrenamiento

Ruta:

```text
docs/agent-training
```

Archivos:

- `prompt-maestro-agente-bpm.md`;
- `playbook-operativo-bpm.md`;
- `rubrica-calidad-bpm.md`;
- `glosario-operativo.md`;
- `datasets/bpm_instruction_dataset.jsonl`;
- `knowledge-distillation-manifest.json`.

## Vault Obsidian

Ruta:

```text
storage/obsidian-bpm-vault
```

Archivo visual principal:

```text
storage/obsidian-bpm-vault/BPM_Knowledge_Graph.canvas
```

Obsidian permite dos vistas:

- `Graph View`: grafo automatico de enlaces entre notas;
- `Canvas`: mapa visual curado para navegar fases, temas y libros.

## Limite importante

Esto no entrena pesos internos de GPT-5.5 ni de ningun LLM local. Lo que se hizo es una destilacion documental persistente: el conocimiento queda estructurado para que el agente lo use como memoria externa.

Este enfoque es el correcto para libros tecnicos grandes porque mantiene trazabilidad, se puede ampliar con mas libros y permite exigir evidencia.

## Siguiente paso tecnico

Implementar busqueda semantica local:

1. generar embeddings de `knowledge_chunks`;
2. guardar vectores en una base local;
3. crear endpoint de busqueda semantica;
4. conectar el prompt maestro con fragmentos recuperados;
5. exigir citas en cada respuesta del agente;
6. registrar supervision humana cuando el agente proponga decisiones de proceso.
