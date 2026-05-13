# ADR 005 - LLM local gratuito para razonamiento y machine learning documental

## Estado

Aceptado.

## Contexto

El proyecto no debe depender de una API pagada de GPT-5.5 para avanzar. El agente necesita:

- razonar sobre procesos complejos;
- trabajar con libros tecnicos en ingles;
- responder en espanol;
- generar aprendizaje documental;
- consultar fuentes con trazabilidad;
- operar localmente cuando sea posible.

La maquina actual tiene aproximadamente 8 GB de RAM y grafica integrada, por lo que no conviene configurar modelos de 32B, 70B o superiores como predeterminados.

## Decision

Usar `Ollama` como runtime local gratuito.

Modelos predeterminados:

```text
Razonamiento: deepseek-r1:1.5b
Embeddings:   qwen3-embedding:0.6b
```

Modelos de mejora para razonamiento mas profundo o mas hardware:

```text
Razonamiento: deepseek-r1:7b, deepseek-r1:14b o deepseek-r1:32b
Embeddings:   qwen3-embedding:4b u 8b
```

## Por que DeepSeek-R1

DeepSeek-R1 es una familia de modelos de razonamiento abierta. Su ficha oficial indica que incluye modelos destilados basados en Qwen y Llama, y que los pesos/codigo de DeepSeek-R1 estan bajo licencia MIT con soporte para uso comercial y derivados.

Para este proyecto se usara la variante local pequena como modo interactivo por restricciones de hardware. `deepseek-r1:7b` queda como modo profundo por lotes; funciona, pero puede ser muy lento en 8 GB de RAM.

Fuente oficial: https://huggingface.co/deepseek-ai/DeepSeek-R1

## Por que Qwen3 Embedding

Qwen3 Embedding esta orientado a embeddings de texto, busqueda semantica, clasificacion, clustering y recuperacion multilingue. Esto encaja con el objetivo del agente: leer libros en ingles y recuperar evidencia para responder en espanol.

Fuente oficial: https://ollama.com/library/qwen3-embedding

## Por que Ollama

Ollama permite ejecutar modelos locales y expone API local compatible con OpenAI, lo que facilita cambiar de proveedor sin reescribir todo el agente.

Fuentes oficiales:

- https://docs.ollama.com/index
- https://docs.ollama.com/openai
- https://docs.ollama.com/api/embed

## Estrategia de aprendizaje

No se hara fine tuning inicial con libros completos.

La estrategia sera:

```text
libros -> fragmentos -> embeddings -> busqueda semantica -> contexto recuperado -> razonamiento con DeepSeek-R1 -> respuesta con citas
```

Esto permite machine learning documental real sin perder trazabilidad.

## Consecuencias

Ventajas:

- no requiere pago por API;
- datos y libros permanecen locales;
- se puede cambiar de modelo despues;
- permite RAG y aprendizaje incremental;
- habilita supervision humana con evidencia.

Limitaciones:

- el rendimiento depende del hardware local;
- modelos pequenos razonan menos que modelos frontier;
- la primera descarga de modelos puede tomar tiempo y espacio en disco;
- la calidad final dependera de embeddings, recuperacion, prompts y evaluacion.

## Implementacion inicial

Backend:

```text
GET /api/local-llm/profile
```

Scripts:

```text
scripts\install-ollama.cmd
scripts\start-ollama.cmd
scripts\pull-local-llm-models.cmd
```
