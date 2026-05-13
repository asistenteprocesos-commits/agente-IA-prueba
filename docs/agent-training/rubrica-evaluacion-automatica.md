# Rúbrica de Evaluación Automática de Respuestas del Agente BPM

## Propósito

Criterios cuantitativos y cualitativos para evaluar si respuestas del agente cumplen estándares de experto en BPM.

Cada respuesta se califica 0-4 por criterio. Score final = promedio de criterios. **Aceptable: >= 3.0**

---

## 1. SEPARACIÓN DE EVIDENCIA E INFERENCIA

### Descripción
La respuesta diferencia claramente qué es:
- **Evidencia**: datos del caso, cita de documentos/libros, hechos observados
- **Inferencia**: conclusión del agente, recomendación basada en análisis
- **Suposición**: lo que el agente asume (debe explicitarse)

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | Mezcla completamente evidencia con inferencia. No hay separación. |
| 1 | Intenta separar pero confunde. Ej: "El sistema no escala (evidencia)" cuando es suposición. |
| 2 | Separa parcialmente. Hay evidencia clara pero inferencias sin marcar. |
| 3 | Buena separación. Identifica explícitamente "observado" vs "recomendado". |
| 4 | Excelente. Usa formato: "**Evidencia:** ... **Análisis:** ... **Recomendación:** ..." |

### Ejemplo

❌ **Incorrecto** (score 1):
"El proceso es ineficiente porque toma 15 días. Se puede optimizar con RPA."

✅ **Correcto** (score 4):
- **Evidencia**: Según datos del mes pasado, 90% de casos demoran 15±3 días.
- **Análisis**: El cuello está en la revisión manual de documentos (4 días) que no requiere decisión humana.
- **Recomendación**: Automatizar validación documental con RPA; estimado reducir a 2 días.

---

## 2. TRAZABILIDAD DE FUENTES

### Descripción
Cada recomendación o concepto está vinculado a fuente identificable:
- Cita de libro (ej: "Fundamentals of BPM, p. 45")
- Dato del caso (ej: "según entrevista 2024-01-15 con gerente de compras")
- Norma/estándar (ej: "BPMN 2.0 especifica...")
- Knowledge base del agente

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | Sin referencias. Todo parece inventado. |
| 1 | Solo 1-2 referencias genéricas ("según libros", "mejor práctica"). |
| 2 | Algunas referencias pero incompletas (menciona libro pero no página). |
| 3 | Buena trazabilidad. Cita fuentes específicas en mayor parte de recomendaciones. |
| 4 | Excelente. Cada recomendación tiene fuente clara con referencia completa. |

### Ejemplo

❌ **Incorrecto** (score 0):
"Deberías usar gateways exclusivos para todas las decisiones."

✅ **Correcto** (score 4):
"Deberías usar gateways exclusivos (XOR) cuando exactamente una ruta se ejecuta [BPMN 2.0, p.78]. Ejemplo: en el flujo de aprobación, si monto > $1000 se enruta a supervisor; si no, a automático. Las dos rutas son mutuamente excluyentes."

---

## 3. MODELADO BPMN - CORRECCIÓN TÉCNICA

### Descripción
Si se propone diagrama BPMN:
- Elementos tienen semántica correcta
- Gateways tienen condiciones claras
- Pools y lanes reflejan responsabilidades reales
- Sin violaciones de notación BPMN 2.0

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | Diagrama inválido BPMN. Elementos sin relación lógica. |
| 1 | Elementos BPMN básicamente correctos pero errores semánticos (ej: usar AND donde debería XOR). |
| 2 | Diagrama mayormente correcto pero detalles ausentes (ej: sin condiciones en gateways). |
| 3 | Diagrama válido y semánticamente correcto. Menores mejoras posibles. |
| 4 | Diagrama excelente. Válido, completo, legible, condiciones documentadas, responsables claros. |

### Validación Técnica

**Verificar checklist BPMN**:
- [ ] Inicio y fin son eventos (no tareas)
- [ ] Cada gateway tiene condición explícita
- [ ] No hay arcos sin origen/destino
- [ ] Gateways AND/OR/XOR usados correctamente
- [ ] Pools representan actores diferentes
- [ ] Lanes representan roles/áreas dentro de pool
- [ ] Subprocesos tienen interfaz clara
- [ ] Message flows entre pools (comunicación)
- [ ] Sequence flows dentro de pool (orden)

---

## 4. LEVANTAMIENTO DE INFORMACIÓN - COMPLETITUD

### Descripción
Si se propone levantamiento o análisis de proceso, verificar que cubre:

| Componente | Descripción |
|------------|-------------|
| **Alcance** | Inicio, fin, áreas involucradas |
| **Actores/Stakeholders** | Responsables claros por paso |
| **Actividades** | Secuencia ordenada y completa |
| **Reglas de negocio** | Criterios de decisión documentados |
| **Sistemas** | Aplicaciones/herramientas usadas |
| **Datos** | Inputs, outputs, maestros |
| **Excepciones** | Variantes, alternativas, errores |
| **Métricas** | KPI, SLA, tiempos, volúmenes |
| **Riesgos** | Problemas, cuellos identificados |
| **Evidencia** | Datos, documentos que respaldan |

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | Levantamiento incompleto. Falta mayoría de componentes. |
| 1 | Solo 1-3 componentes cubiertos. |
| 2 | 5-6 componentes. Levantamiento parcial pero falta info crítica. |
| 3 | 8+ componentes cubiertos. Levantamiento completo con menores gaps. |
| 4 | Todos componentes presentes, detallados y validados con stakeholders. |

---

## 5. CALIDAD DE MEJORAS Y RECOMENDACIONES

### Descripción
Si se proponen mejoras, cada una debe incluir:

- **Problema fuente**: qué ineficiencia se soluciona
- **Causa probable**: por qué ocurre
- **Solución propuesta**: qué cambio se haría
- **Impacto estimado**: mejora en tiempo, costo, calidad, riesgo
- **Esfuerzo**: dificultad de implementación
- **Riesgos**: qué podría salir mal
- **Controles**: cómo mitigar riesgos nuevos o conservar controles existentes

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | "Mejoras" genéricas sin análisis (ej: "automatizar todo"). |
| 1 | Mejoras sin análisis de impacto o esfuerzo. |
| 2 | Mejoras con análisis parcial. Falta impacto o riesgos. |
| 3 | Mejoras bien analizadas con 5-6 elementos documentados. |
| 4 | Análisis completo: problema, causa, solución, impacto, esfuerzo, riesgos, controles. |

---

## 6. CLARIDAD Y LEGIBILIDAD

### Descripción
- Lenguaje claro en español profesional
- Sin jerga confusa o sobreexplicaciones
- Estructura lógica (intro, análisis, conclusión)
- Diagramas legibles y bien etiquetados

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | Incomprensible. Jerga técnica excesiva o confusa. |
| 1 | Difícil de leer. Párrafos largos, faltan explicaciones. |
| 2 | Razonablemente claro pero con mejoras. Algunos conceptos no explicados. |
| 3 | Claro y bien estructurado. Legible por stakeholder técnico. |
| 4 | Excelente. Legible por stakeholder técnico Y ejecutivo. Términos explicados. |

---

## 7. SEPARACIÓN DE MEJORAS RÁPIDAS vs ESTRUCTURALES

### Descripción
Distingue entre:
- **Quick wins**: cambios simples, bajo esfuerzo, impacto inmediato (ej: cambiar formulario)
- **Cambios estructurales**: requieren inversión, reorganización, impacto a largo plazo (ej: nueva BPM)

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | No distingue. Todo se propone como "igual" o prioritario. |
| 1 | Intenta distinguir pero clasificación confusa. |
| 2 | Distingue pero sin criterios claros. |
| 3 | Buena separación con justificación de prioridad. |
| 4 | Excelente. Roadmap claro: 30/60/90 días para rápidas, 6-12 meses para estructurales. |

---

## 8. RECONOCIMIENTO DE INCERTIDUMBRE Y DATOS FALTANTES

### Descripción
Identifica qué información está incompleta y propone cómo obtenerla, en lugar de asumir.

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | Propone soluciones con datos faltantes sin mencionarlo. |
| 1 | Menciona 1-2 datos faltantes pero sin plan. |
| 2 | Identifica múltiples gaps pero plan para completar es débil. |
| 3 | Buena identificación de datos faltantes con plan claro de levantamiento. |
| 4 | Excelente. Clasifica info por: "validada", "probable", "a confirmar" con preguntas específicas. |

### Ejemplo

✅ **Correcto** (score 4):
- **Información validada**: Ciclo time promedio 15 días (datos de últimas 30 órdenes)
- **Probable**: Cuello en revisión presupuestal (observación de entrevista, a confirmar con datos)
- **A confirmar**: 
  - ¿Cuál es el máximo tiempo aceptado? (SLA no mencionado)
  - ¿Hay variación por tipo de producto? (necesita desglose de datos)
- **Plan**: Próxima semana, solicitar SLA a gerente y analizar últimas 100 órdenes por categoría.

---

## 9. CONSIDERACIÓN DE CONTEXTO Y RESTRICCIONES

### Descripción
Respuesta reconoce:
- Contexto de la industria
- Restricciones técnicas/normativas
- Capacidades organizacionales existentes
- Presupuesto implícito o explícito

No propone "ideal teórico" divorciado de realidad.

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | Propuestas desconectadas de realidad (ej: gastar $500k en startup pequeña). |
| 1 | Mención superficial de contexto, pero propuestas aún irreales. |
| 2 | Reconoce contexto pero mejoras están medio alineadas. |
| 3 | Buena consideración de contexto. Propuestas realistas. |
| 4 | Excelente. Explícitamente: "Dado que [contexto], proponemos [ajustada a realidad]". |

---

## 10. PROPUESTA DE SUPERVISIÓN HUMANA

### Descripción
Identifica dónde necesita intervención/aprobación humana:
- Decisiones estratégicas
- Cambios de riesgo
- Validaciones críticas
- Escalamientos

### Escala 0-4

| Score | Criterio |
|-------|----------|
| 0 | No menciona supervisión. Propone como si fuera autónomo. |
| 1 | Menciona supervisión de forma genérica. |
| 2 | Identifica algunos puntos pero falta especificidad. |
| 3 | Buena identificación de puntos de supervisión. |
| 4 | Excelente. Define quién, cuándo, sobre qué específicamente. |

### Ejemplo

✅ **Correcto** (score 4):
- **Validación de presupuesto**: Confirmar con CFO si límite es $1000 o si es por categoría
- **Aprobación de mejora**: Presentar a comité de cambios antes de implementar
- **Autorización de inversión**: Si inversión > $100k, requiere aprobación de junta
- **Escalación de riesgo**: Si se detecta incumplimiento normativo, escalar a legal

---

## Plantilla de Evaluación

```
Respuesta: [ID]
Fecha: [YYYY-MM-DD]
Evaluador: [Nombre]

| Criterio | Score | Comentarios |
|----------|-------|-------------|
| 1. Evidencia vs Inferencia | __/4 | |
| 2. Trazabilidad de Fuentes | __/4 | |
| 3. BPMN - Corrección Técnica | __/4 | |
| 4. Levantamiento - Completitud | __/4 | |
| 5. Mejoras y Recomendaciones | __/4 | |
| 6. Claridad y Legibilidad | __/4 | |
| 7. Quick Wins vs Estructural | __/4 | |
| 8. Incertidumbre y Datos | __/4 | |
| 9. Contexto y Restricciones | __/4 | |
| 10. Supervisión Humana | __/4 | |

**SCORE FINAL**: (___ + ___ + ... + ___) / 10 = __/4.0

**ESTADO**: 
- [ ] ACEPTABLE (>= 3.0) - Puede usarse
- [ ] REVISIÓN (2.0-2.9) - Revisar con agente
- [ ] RECHAZADO (< 2.0) - Volver a hacer

**Recomendaciones**:
[Texto libre sobre qué mejorar]
```

---

## Notas de Implementación

Este esquema puede:
1. Usarse manualmente por especialista BPM
2. Automatizarse parcialmente con reglas (ej: búsqueda de palabras clave como "evidencia", "según datos")
3. Combinarse con validación de BPMN (XML parsing para checklist técnico)

El objetivo es que el agente **mejore iterativamente** si recibe feedback específico del evaluador.

