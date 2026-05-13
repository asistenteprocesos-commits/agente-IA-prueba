# Antipatrones y Errores Comunes en Levantamiento de Procesos

## Propósito

Este documento enseña al agente a identificar y evitar errores típicos en análisis y modelado BPMN. Cada antipatrón incluye: definición, síntoma, causa raíz, consecuencia y remedio.

---

## 1. Proceso Sin Fin Claro

### Definición
El proceso no tiene un evento de fin explícito o claro. Las actividades "simplemente terminan" sin cierre formal.

### Síntomas
- "Cuando el cliente recibe el producto, se acaba"
- Último evento es tarea, no evento
- No hay consenso sobre cuándo el caso está verdaderamente "completo"

### Causa Raíz
- No involucrar todas las áreas en levantamiento
- Enfoque solo en actividades operativas, no en cierre
- Confundir "enviar algo" con "fin del proceso"

### Consecuencia
- No se registra cierre en sistemas
- Ciclo time incorrecto (se cuenta desde inicio a envío, no a confirmación de entrega)
- Falta control sobre qué pasó al final
- Difícil hacer follow-up o garantía

### Remedio
**Preguntas de levantamiento**:
- "¿Cómo sabe el negocio que el caso está completo?"
- "¿Quién registra la finalización?"
- "¿Hay pasos de cierre, reconciliación, archivo?"
- "¿Qué documenta el cierre? (email, registro en sistema, firma)"

**En BPMN**:
```
INCORRECTO:
[Enviar producto] (sin fin claro)

CORRECTO:
[Enviar producto]
-> [Evento: Producto entregado y confirmado por cliente]
-> {¿Confirmación recibida?}
     ├─ Sí -> [Evento fin: Caso cerrado exitosamente]
     └─ No -> [Evento fin: Caso expirado por timeout]
```

---

## 2. Gateway Sin Condiciones o Condiciones Implícitas

### Síntomas
```
INCORRECTO: "¿Aprobado?" (sin especificar criterio)

CORRECTO: "¿Monto <= $1000 Y Usuario cumple 6 meses?" 
```

### Causa Raíz
- El usuario conoce la regla "por la cabeza" pero no la verbaliza
- Falta de documentación formal de criterios de negocio
- No preguntar "por qué se toma esa decisión"

### Consecuencia
- Inconsistencia en decisiones
- Riesgo de cumplimiento (decisiones no trazables)
- Imposible automatizar
- Entrenamientos new hire son imperfectos

### Remedio
**Siempre preguntar**:
- "¿Cuál es la condición exacta para cada rama?"
- "¿Hay fórmula, regla, tabla?"
- "¿Ha habido casos que no cumplen la regla esperada?"

**Documentar en matriz**:
| Condición | Si verdadero | Si falso |
|-----------|-------------|---------|
| Monto <= $1000 | Aprobación automática | A supervisor |

---

## 3. Omitir Caminos Alternativos (Solo Happy Path)

### Síntoma
El modelo muestra solo el caso "normal" sin excepciones, errores o rechazos.

### Causa Raíz
- Enfoque en "cómo debería ser" no en "cómo es"
- No preguntar por excepciones
- Baja representación de áreas de soporte/excepciones en levantamiento

### Consecuencia
- Modelo no coincide con realidad observada en datos
- Process mining mostrará múltiples variantes no modeladas
- Personal no ve reflejo de su trabajo real
- SLA y métricas no incluyen tiempo de excepción

### Remedio
**Preguntas obligatorias**:
- "¿Qué pasa si [condición falla]?"
- "¿Cuál es el porcentaje de rechazos/excepciones?"
- "¿Dónde se hacen retrabajes (rework)?"
- "¿Qué hace el equipo el 10% de los casos difíciles?"

**En BPMN**:
```
[Procesar]
-> {¿Validación OK?}
     ├─ Sí -> [Continuar]
     └─ No -> [Enviar a corrección] <- Camino alternativo visible
              -> [Reintento]
              -> {¿OK en 2º intento?}
```

---

## 4. Falta de Responsables (Actividades Sin Lane)

### Síntoma
Actividad sin claridad de quién la hace. En BPMN: tarea fuera de lane o sin asignación.

### Causa Raíz
- Levantamiento incompleto (no incluir a todos los áreas)
- Actividad compartida (varios hacen según contexto)
- Ambigüedad: ¿Es RRHH o Manager?

### Consecuencia
- En implementación, no se sabe a quién asignar
- Nadie se siente responsable -> tareas se pierden
- Imposible medir carga de trabajo por rol
- Automación incompleta

### Remedio
**Preguntar específicamente**:
- "¿Quién completa esta tarea?"
- "¿Siempre la misma persona?"
- "¿A qué rol o área le corresponde?"
- "¿Hay casos donde la hace persona diferente? ¿Por qué?"

---

## 5. Inputs/Outputs No Definidos

### Síntoma
- "Se procesa la solicitud" (¿de dónde viene? ¿qué formato?)
- "Se aprueba" (¿quién envía aprobación? ¿por email, sistema?)"

### Causa Raíz
- No mapear flujo de datos
- No documentar fuente de información
- Asumir que "el sistema lo hace"

### Consecuencia
- Al integrar sistemas, quedan gaps
- Datos duplicados en múltiples lugares
- Imposible rastrear origen de un dato (data lineage)
- RPA/automatización incompleta

### Remedio
**Para cada tarea preguntar**:
- "¿De dónde llega la información?" (email, portal, API, base de datos)
- "¿En qué formato?" (Excel, PDF, estructura, campo de sistema)
- "¿Quién la envía?" (cliente, otro proceso, archivo batch)
- "¿Dónde se registra el resultado?" (sistema, email, documento)

**En BPMN, usar objetos de datos**:
```
[Solicitud en email] --data flow--> [Procesar solicitud]
[Procesar solicitud] --data flow--> [Orden en BD]
```

---

## 6. Ciclos Infinitos Sin Criterio de Salida

### Síntoma
```
INCORRECTO:
[Revisar] -> {¿OK?} -> No -> [Corregir] -> (vuelve a Revisar, sin fin)
```

### Causa Raíz
- No documentar criterio de "cuando se detiene"
- Repeticiones no acotadas
- No reconocer máximo de reintentos

### Consecuencia
- En simulación: ciclos infinitos
- En datos: casos atascados en actividad
- Presupuesto de tiempos impreciso

### Remedio
**Siempre especificar**:
- "¿Cuál es el máximo de reintentos?" (por defecto: 3)
- "¿Cuándo se escala vs. se reintenta?"
- "¿Hay timeout?" (ej: si no se corrige en 5 días, escalar)

**En BPMN**:
```
CORRECTO:
[Revisar] -> {¿OK?}
    ├─ Sí -> [Siguiente]
    └─ No -> [Contador de intentos] -> {¿Intentos < 3?}
                ├─ Sí -> [Enviar a corrección] -> (vuelve a Revisar)
                └─ No -> [Escalar a supervisor]
```

---

## 7. Nomenclatura Ambigua de Actividades

### Síntoma
- "Procesar" (¿qué se procesa exactamente?)
- "Revisar" (¿qué se revisa? ¿por quién? ¿qué criterio?)
- "Administrar" (demasiado genérico)

### Causa Raíz
- Falta de convención de nombrado
- Nombres jerárquicos (proceso, subproceso, tarea no diferenciados)
- Nombres demasiado técnicos O demasiado vagos

### Consecuencia
- Confusión al leer modelo
- Ambigüedad en asignación
- Difícil traducir a sistema
- Training de personal ineficiente

### Remedio
**Regla**: Verbo + Objeto, específico, de 2-5 palabras.

| Incorrecto | Correcto |
|-----------|---------|
| Procesar | Validar monto contra presupuesto disponible |
| Revisar | Revisar factura por completitud y coincidencia de datos |
| Admin | Registrar movimiento en contabilidad |
| Hacer | Asignar soporte técnico según disponibilidad |

---

## 8. Subprocesos Demasiado Grandes o Demasiado Pequeños

### Síntomas
**Demasiado grande**:
- Subproceso con 20+ tareas adentro
- Difícil de leer
- No se puede reutilizar porque es específico de un contexto

**Demasiado pequeño**:
- Subproceso con 1 sola tarea
- Overhead de abstracción
- No suma valor

### Remedio
**Heurístico**:
- Subproceso = 3-7 tareas relacionadas logicamente
- Tiene interfaz clara (inputs, outputs)
- Es reutilizable (usado en >= 2 procesos)

---

## 9. Mixing Responsabilidades en una Lane

### Síntoma
Lane "Operaciones" contiene: [Recibir], [Procesar], [Transportar], [Entregar]
Pero en realidad: Recibir es Almacén, Transportar es Logística, Entregar es Cliente.

### Remedio
- Lane = Responsable o rol específico
- Si actividades son responsabilidad diferente, crear lanes diferentes
- Usar message flows entre pools si son áreas separadas

---

## 10. Confundir Datos con Lógica de Negocio

### Síntoma
- Modelar "guardar en BD" como tarea visible en BPMN
- Modelar "enviar email de confirmación" como tarea central

### Remedio
- Tareas en BPMN = decisiones y trabajo de negocio
- Guardar datos es "implicado" en la tarea, no tarea separada
- Notificaciones (emails, SMS) modelas como eventos o subprocesos, no tareas principales

---

## Checklist de Validación Durante Levantamiento

Usar este checklist al terminar entrevista/taller:

- [ ] Cada actividad tiene responsable claro (nombre de rol/área, no persona)
- [ ] Cada gateway tiene condición explícita (escrita, no implícita)
- [ ] Todos los caminos alternativos (excepciones) están identificados
- [ ] Entrada a proceso está clara (trigger, evento)
- [ ] Salida/cierre del proceso tiene evento terminal
- [ ] Inputs y outputs de cada tarea están documentados
- [ ] Ciclos tienen criterio de salida y máximo de iteraciones
- [ ] Actividades tienen nombres específicos y comprensibles
- [ ] Tiempos estimados (ciclo time, SLA) están validados
- [ ] Métricas o KPI del proceso están claros
- [ ] Problemas identificados están documentados con evidencia
- [ ] Stakeholders validan que modelo es fiel a realidad
- [ ] Datos históricos o event logs coinciden con modelo (>90%)

---

## Ejercicio: Identificar Antipatrones

Dado el siguiente fragmento incorrecto, identifique mínimo 3 antipatrones:

```
Pool: Compras

[Inicio: Solicitud]
-> [Procesar]
-> [Revisar]
-> [Fin]
```

**Respuesta**: 
1. Sin responsables (no hay lanes)
2. Nombres ambigüos (Procesar, Revisar ¿qué exactamente?)
3. Solo happy path (sin condiciones, sin excepciones)
4. Sin inputs/outputs definidos
5. Sin criterios de decisión visibles
6. Fin sin condición (¿siempre aprobado?)

