# Paquete de entrenamiento documental del agente BPM

Este paquete convierte los libros procesados en memoria operativa para el agente.

No modifica pesos de un LLM. Es una destilacion documental: prompts, playbooks, reglas, dataset y trazabilidad para que un LLM local o GPT use la biblioteca como conocimiento externo.

## Archivos

- `prompt-maestro-agente-bpm.md`: instrucciones base del agente.
- `playbook-operativo-bpm.md`: metodologia de gestion de casos.
- `rubrica-calidad-bpm.md`: criterios de revision de respuestas y entregables.
- `glosario-operativo.md`: vocabulario minimo del agente.
- `datasets/bpm_instruction_dataset.jsonl`: ejemplos de instruccion/respuesta para evaluacion o futuro fine tuning.
- `knowledge-distillation-manifest.json`: resumen de volumen y fuentes.

## Uso desde el software

El backend expone este paquete en:

```text
GET /api/knowledge/agent-training-profile
```

El frontend muestra el resumen en la seccion `Conocimiento`, bloque `Memoria del agente`.

## Vista visual

El grafo navegable esta en:

```text
storage/obsidian-bpm-vault
```

Abrir en Obsidian como vault y luego abrir `BPM_Knowledge_Graph.canvas`.

## Fuente

- Libros procesados: 2
- Paginas procesadas: 1279
- Caracteres extraidos: 3256114
- Insights estructurados: 5614
- Metodologia: 8 fases
