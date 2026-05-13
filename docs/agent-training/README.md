# Paquete de entrenamiento documental del agente BPM

Este paquete convierte los libros procesados en memoria operativa para el agente.

No modifica pesos de un LLM. Es una destilacion documental: prompts, playbooks, reglas, dataset y trazabilidad para que un LLM local o GPT use la biblioteca como conocimiento externo.

## Archivos

### Documentación Principal
- `prompt-maestro-agente-bpm.md`: instrucciones base del agente con 8 fases metodologicas.
- `playbook-operativo-bpm.md`: metodologia de gestion de casos (detallado por fase).
- `rubrica-calidad-bpm.md`: criterios de revision de respuestas y entregables.

### Referencia Técnica (Nuevos)
- `glosario-operativo.md`: 150+ términos especializados en BPM, BPMN, process mining, análisis cuantitativo, riesgos, transformación digital e industrias específicas.
- `patrones-bpmn.md`: 10 patrones BPMN con ejemplos prácticos, comparaciones correcto/incorrecto y checklist de validación.
- `casos-bpmn-completos.md`: 10 casos reales (solicitud de compra, reclamos, onboarding, etc) con narrativa as-is/to-be, diagramas, métricas e impacto.
- `antipatrones-errores-comunes.md`: 10+ antipatrones identificables durante levantamiento con causa/remedio.

### Datasets y Configuración
- `datasets/bpm_instruction_dataset.jsonl`: ejemplos de instrucción/respuesta para evaluación o futuro fine tuning.
- `datasets/bpm_extended_examples.jsonl`: ejemplos avanzados sobre BPMN, process mining, trazabilidad, riesgos y supervisión.
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
