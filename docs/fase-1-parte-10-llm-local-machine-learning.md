# Fase 1 - Parte 10 - LLM local y machine learning documental

## Objetivo

Preparar el proyecto para usar un LLM gratuito/local en lugar de una API GPT de pago.

Esta fase conecta la base documental con una arquitectura de aprendizaje local:

```text
DeepSeek-R1 -> razonamiento BPM
Qwen3 Embedding -> vectores y busqueda semantica
Ollama -> runtime local
```

## Estado implementado

- configuracion backend para Ollama;
- modelo razonador local predeterminado;
- modelo de embeddings predeterminado;
- endpoint de perfil local;
- vista en frontend para estado del LLM local;
- scripts de instalacion, inicio y descarga de modelos;
- ADR tecnica de decision.

## Endpoint

```text
GET /api/local-llm/profile
```

El endpoint informa:

- si Ollama esta instalado;
- si el servidor local esta activo;
- que modelos debe descargar;
- que modelos ya existen localmente;
- estrategia de aprendizaje documental;
- acciones pendientes.

## Modelos seleccionados

Predeterminado para esta maquina:

```text
deepseek-r1:1.5b
qwen3-embedding:0.6b
```

Modo profundo o upgrade futuro:

```text
deepseek-r1:7b
deepseek-r1:14b
qwen3-embedding:4b
```

## Como activarlo

Instalar o verificar Ollama:

```powershell
.\scripts\install-ollama.cmd
```

Iniciar Ollama:

```powershell
.\scripts\start-ollama.cmd
```

Descargar modelos:

```powershell
.\scripts\pull-local-llm-models.cmd
```

## Como cambiar modelos

Antes de descargar modelos, se pueden definir variables:

```powershell
$env:OLLAMA_REASONING_MODEL="deepseek-r1:14b"
$env:OLLAMA_EMBEDDING_MODEL="qwen3-embedding:4b"
.\scripts\pull-local-llm-models.cmd
```

En esta maquina tambien quedo descargado `deepseek-r1:7b`, pero debe usarse para analisis por lotes o tareas donde se pueda esperar mas tiempo.

## Machine learning esperado

La siguiente implementacion debe:

1. generar embeddings para cada `knowledge_chunk`;
2. guardar vectores localmente;
3. crear busqueda semantica por pregunta, tema, caso y fase;
4. recuperar fragmentos relevantes antes de responder;
5. pedir al LLM local que razone solo con esos fragmentos;
6. entregar respuesta en espanol con citas y nivel de confianza.

## Entrenamiento vs aprendizaje local

En esta etapa, "entrenamiento" significa aprendizaje documental operativo:

- extraccion de conocimiento;
- embeddings;
- dataset de instrucciones;
- prompts y reglas;
- recuperacion semantica;
- evaluacion de respuestas.

No significa modificar pesos internos del modelo. Eso se evaluara despues si existe un dataset propio validado por expertos.
