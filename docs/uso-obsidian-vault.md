# Uso del vault Obsidian BPM

## Objetivo

El vault de Obsidian es la vista grafica y navegable de la memoria documental del agente.

No es solo programacion interna: se puede abrir visualmente en Obsidian para ver relaciones entre libros, fases metodologicas, temas, glosario y trazabilidad.

## Ruta del vault

```text
storage/obsidian-bpm-vault
```

En esta maquina, la ruta completa es:

```text
c:\Users\Espana\Documents\agente IA prueba\storage\obsidian-bpm-vault
```

## Como abrirlo

1. Abre Obsidian.
2. Selecciona `Open folder as vault`.
3. Elige la carpeta `storage/obsidian-bpm-vault`.
4. Abre `00_Inicio.md` para entrar por el indice principal.
5. Abre `BPM_Knowledge_Graph.canvas` para ver el mapa visual curado.
6. Usa `Graph View` de Obsidian para ver el grafo automatico de enlaces.

## Que contiene

- mapa de libros procesados;
- metodologia maestra BPM en 8 fases;
- temas principales;
- glosario BPM, BPMN y process mining;
- red de conocimiento;
- trazabilidad hacia fuentes y fragmentos;
- canvas visual para navegar conceptos.

## Diferencia entre Graph View y Canvas

`Graph View` es el grafo automatico de Obsidian. Muestra las conexiones entre notas mediante enlaces `[[...]]`.

`BPM_Knowledge_Graph.canvas` es un mapa visual disenado para el proyecto. Organiza las fases, libros y temas de forma mas clara para revision humana.

## Nota importante

El vault no debe copiar libros completos en Markdown. Para respetar trazabilidad y evitar duplicacion innecesaria, los textos completos quedan en la base documental local y en fragmentos internos del sistema. Obsidian muestra el mapa de conocimiento, los indices, temas, fases y enlaces de trabajo.

## Uso por el agente

El agente debe usar esta memoria como apoyo, pero la consulta operativa principal debe avanzar hacia:

```text
fragmentos de libros -> embeddings -> busqueda semantica -> contexto recuperado -> respuesta con citas
```

La siguiente implementacion tecnica sera conectar embeddings locales para que el agente recupere fragmentos relevantes antes de responder.
