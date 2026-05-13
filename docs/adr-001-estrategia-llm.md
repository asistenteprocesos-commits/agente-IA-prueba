# ADR 001 - Estrategia de LLM

## Estado

Propuesto

## Fecha

2026-05-12

## Decision

Adoptar una estrategia hibrida de modelos:

1. `Gemini 2.5 Flash-Lite` como modelo principal gratuito para el MVP.
2. `Gemma 3` o `Qwen3` via `Ollama` como respaldo local y capa privada.

## Contexto

El producto necesita:

- contexto largo para documentos;
- buena capacidad de extraccion y estructuracion;
- salida JSON;
- function calling o tool use;
- costos cercanos a cero para el arranque;
- posibilidad de operar con informacion sensible.

Ningun modelo gratuito unico cubre bien todos esos requisitos de forma permanente. Por eso la decision correcta es desacoplar el proveedor de la logica del agente.

## Motivos

### Gemini 2.5 Flash-Lite

Se elige para el MVP porque:

- existe capa gratuita publica;
- soporta contexto largo;
- se integra bien con flujos agenticos y salidas estructuradas;
- sirve para entrevistas, clasificacion de hallazgos, consolidacion y coordinacion.

### Gemma 3 o Qwen3 por Ollama

Se eligen como segunda capa porque:

- pueden correr localmente;
- reducen riesgo de exponer documentos sensibles;
- permiten continuidad cuando la capa gratuita del proveedor tenga limites;
- facilitan pruebas y despliegues controlados.

## Consecuencias

### Positivas

- menor costo inicial;
- arquitectura portable;
- mayor privacidad;
- resiliencia ante limites de cuota;
- posibilidad de comparar calidad entre modelos.

### Negativas

- mayor complejidad de integracion;
- necesidad de evaluar modelos por caso de uso;
- posible diferencia de calidad entre nube y local.

## Regla operativa recomendada

- usar modelo en nube para coordinacion, clasificacion y extraccion general;
- usar modelo local para material sensible y revisiones privadas;
- exigir evidencia antes de aceptar conclusiones del agente;
- registrar modelo, version, prompt y salida por cada paso relevante.

## Decision de implementacion

Definir desde el inicio una interfaz `ModelProvider` para cambiar entre proveedores sin reescribir el orquestador.
