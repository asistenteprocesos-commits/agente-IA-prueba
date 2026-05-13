# Patrones BPMN - Guía de Modelado Correcto

Este documento describe patrones BPMN aplicados a problemas reales, con ejemplos de lo correcto y antipatrones.

## 1. Decisiones Simples (Gateway Exclusivo - XOR)

### Caso: Aprobación de Solicitud de Compra

**Cuando usar**: Una variable determina un único camino de ejecución.

**Patrón correcto**:
```
[Inicio] -> [Revisar monto] -> {Gateway XOR}
                                  ├─ SI monto <= $1000 -> [Aprobación automática]
                                  └─ NO monto > $1000 -> [Enviar a aprobador]
                               -> [Registrar decisión] -> [Fin]
```

**Características**:
- Gateway tiene nombre claro: "¿Monto <= $1000?"
- Condiciones son exhaustivas (cubren todos los casos)
- Exactamente un camino se ejecuta por caso
- Ambos caminos convergen en punto común

**Antipatrón**:
- Gateway sin condiciones explícitas (condiciones en la cabeza del usuario)
- Múltiples caminos convergentes sin sincronización
- Omitir casos edge (¿qué pasa con monto = 0?)

---

## 2. Decisiones Múltiples e Independientes (Gateway Inclusivo - OR)

### Caso: Notificaciones en Paralelo

**Cuando usar**: Una o más condiciones independientes determinan múltiples caminos que pueden ejecutarse en paralelo.

**Patrón correcto**:
```
[Crear orden] -> {Gateway OR}
                  ├─ SI aplica descuento -> [Aplicar descuento]
                  ├─ SI es cliente VIP -> [Generar reporte VIP]
                  ├─ SI es envío express -> [Priorizar envío]
              -> {Gateway OR de convergencia}
              -> [Confirmar orden] -> [Fin]
```

**Características**:
- Múltiples caminos pueden ejecutarse
- Caminos son independientes (no interfieren)
- Convergencia espera a todos los caminos completados
- Útil para notificaciones, reúpliques de datos

**Antipatrón**:
- Usar OR cuando debería ser AND (ejecutar todo)
- Usar OR cuando debería ser XOR (ejecutar solo uno)

---

## 3. Trabajo Paralelo (Gateway AND)

### Caso: Procesamiento Simultáneo de Documentos

**Patrón correcto**:
```
[Iniciar solicitud] -> {Gateway AND}
                       ├─ [Revisar documento fiscal]
                       ├─ [Validar identidad]
                       └─ [Verificar saldo]
                    -> {Gateway AND de sincronización}
                    -> [Tomar decisión] -> [Fin]
```

**Características**:
- Todas las tareas inician simultáneamente
- No hay dependencia entre caminos
- La siguiente tarea espera a que TODOS terminen
- Usado para actividades que pueden paralelizarse

**Cálculo de tiempo**:
- Tiempo total = máximo(rama1, rama2, rama3), NO suma
- Si rama1 = 5 min, rama2 = 10 min, rama3 = 3 min
- Tiempo total = 10 min (no 18 min)

---

## 4. Procesos Iterativos (Bucles)

### Caso: Revisión de Calidad con Ciclos

**Patrón correcto**:
```
[Recibir documento] -> [Primera revisión] -> {Gateway}
                                              ├─ Aprobado -> [Archivo]
                                              └─ Rechazado -> [Enviar a corrección] -> (vuelve a Recibir)
                                                                                        [Fin]
```

**Mejor patrón con subconsideración **:
```
[Recibir documento]
  -> [Subproceso: Ciclo de revisión]
       -> [Revisar]
       -> {¿Aprobado?}
            ├─ Sí -> [Fin subproceso]
            └─ No -> [Corregir] -> (vuelve a Revisar)
  -> [Archivo] -> [Fin]
```

**Características**:
- El flujo vuelve a tarea anterior, no a inicio
- Usar subproceso para encapsular ciclo
- Definir criterio de salida claro
- Considerar máximo de iteraciones para evitar bucles infinitos

---

## 5. Subprocesos y Reutilización

### Caso: Solicitud de Compra con Subprocesos

**Patrón correcto**:
```
[Crear solicitud]
  -> [Subproceso: Validación]
       (Valida disponibilidad, presupuesto, cumplimiento)
  -> {¿Validación OK?}
       ├─ Sí -> [Subproceso: Aprobación]
       │           (Enruta a autoridad competente)
       │        -> [Registrar aprobación]
       └─ No -> [Reportar rechazo] -> [Fin]
  -> [Crear orden de compra] -> [Fin]
```

**Ventajas**:
- Reutilización: "Validación" se usa en múltiples procesos
- Versionado centralizado
- Mejora legibilidad de proceso principal
- Facilita testing y auditoría

**Call Activity (Subproceso llamado)**:
- Invoca otro proceso BPMN versioned
- Tiene interface clara: entrada/salida
- Permite governance central de procesos compartidos

---

## 6. Manejo de Excepciones

### Caso: Procesamiento de Pago con Excepciones

**Patrón incorrecto (no documentar excepciones)**:
```
[Recibir pago] -> [Procesar] -> [Fin]
```

**Patrón correcto**:
```
[Recibir pago]
  -> [Validar fondos]
  -> {¿Fondos disponibles?}
       ├─ Sí -> [Procesar pago]
       └─ No -> [Event intermedio: Error de fondos]
                  -> [Notificar cliente] -> [Enviar a revisión manual] -> [Fin alternativo]
  -> {¿Pago exitoso?}
       ├─ Sí -> [Confirmar transacción] -> [Fin OK]
       └─ No -> [Evento intermedio: Error de procesamiento]
                  -> [Registrar fallo] -> [Reintentar] -> (vuelve a Procesar)
                                       -> Si fallos > 3: [Escalar] -> [Fin error]
```

**Características**:
- Todos los caminos (feliz y excepción) documentados
- Criterios claros para cada ruta
- No asumir "nunca falla"
- Incluir compensación si aplica

---

## 7. Compensación y Transacciones

### Caso: Reserva y Pago de Hotel

**Patrón correcto**:
```
[Recibir solicitud]
  -> [Subproceso transaccional]
       -> [Reservar habitación]
       -> [Procesar pago]
            Si falla: -> [Liberar habitación] (compensación)
       -> [Enviar confirmación]
  -> {¿Éxito?}
       ├─ Sí -> [Archivo] -> [Fin OK]
       └─ No -> [Revertir todas] -> [Notificar fallo] -> [Fin error]
```

**Semantica**:
- Subproceso transaccional= si cualquier actividad interna falla, ejecuta compensaciones en reverso
- Compensación no siempre es posible (ej: email enviado no se "desenvía")

---

## 8. Eventos Intermedios (Esperas, Tiempos, Interrupciones)

### Caso: Espera de Confirmación del Cliente

**Patrón correcto**:
```
[Enviar propuesta]
  -> [Evento intermedio: Esperar confirmación o timeout]
       ├─ Confirmación recibida -> [Procesar] -> [Fin OK]
       └─ Timeout (7 días) -> [Enviar recordatorio] -> [Evento: Esperar de nuevo]
                              -> Si aún no: [Archivar como rechazada] -> [Fin]
```

**Tipos**:
- Timer: espera X minutos/días
- Message: espera mensaje específico
- Signal: espera señal de otro proceso
- Escalation: si algo no ocurre, ejecuta acción
- Conditional: si condición se cumple

---

## 9. Pools y Swimlanes (Responsabilidades)

### Caso: Proceso entre Cliente y Empresa

**Patrón correcto**:
```
Pool: Cliente          |  Pool: Empresa
                       |
[Cliente hace pedido]  |
---message flow----->  [Empresa recibe]
                       [Empresa procesa]
                       [Empresa envía confirmación]
<-----message flow---- [Cliente recibe]
[Cliente confirma]     |
```

**Lane (dentro de Empresa)**:
```
Lane: Ventas    | [Recibir] -> [Validar] -> [Confirmar]
Lane: Logística |                           [Preparar envío]
Lane: Finanzas  |                           [Generar factura]
```

**Reglas**:
- Pool = actor principal (organización, sistema)
- Lane = responsable dentro del pool (área, rol)
- Message flow = comunicación entre pools
- Sequence flow = orden dentro del pool

---

## 10. Eventos de Negocio Complejos

### Caso: Procesamiento de Reclamo con Bifurcación de Evento

**Patrón correcto**:
```
[Recibir reclamo]
  -> [Clasificar]
  -> {Tipo de reclamo?}
       ├─ Producto defectuoso -> [Subproceso: Reemplazo]
       ├─ Entrega retrasada -> [Subproceso: Compensación]
       └─ Error en factura -> [Subproceso: Corrección]
  -> [Evento intermedio: Reclamo resuelto O Escalación requerida]
       ├─ Resuelto -> [Archivo] -> [Fin]
       └─ Escalación -> [Enviar a supervisión] -> [Esperar decisión] -> [Archivo] -> [Fin]
```

---

## Checklist de Validación BPMN

Al modelar, verificar:

- [ ] Cada inicio tiene un fin explícito
- [ ] Todas las condiciones en gateways están nombradas
- [ ] No hay actividades con 0 entrada o 0 salida
- [ ] Toda tarea tiene responsable (lane o anotación)
- [ ] Excepciones están modeladas, no asumidas
- [ ] Tiempos de espera son explícitos (eventos)
- [ ] Subprocesos tiene interface clara
- [ ] Message flows muestran comunicación entre sistemas/áreas
- [ ] Lanes reflejan responsabilidad (no duplicar tarea en múltiples lanes)
- [ ] Variantes y casos edge están representados

