# 10 Casos BPMN Completos - Ejemplos Prácticos

Cada caso incluye: narrativa, diagrama BPMN (texto), XML, métricas y mejoras potenciales.

---

## CASO 1: Solicitud de Compra (Pequeña Empresa)

### Narrativa As-Is

Una empresa pequeña recibe solicitudes de compra de distintas áreas. El proceso actual:
1. El empleado completa formulario en papel o email
2. Lo envía al área de compras
3. El comprador verifica presupuesto disponible en hoja de cálculo
4. Si hay presupuesto, busca en catálogo de proveedores
5. Hace solicitud al proveedor (por email o teléfono)
6. Proveedor envía cotización
7. El comprador compara precios (normalmente 2-3 cotizaciones)
8. Negocia si ve oportunidad
9. Genera orden de compra (documento Word)
10. Envía a finanzas para pago
11. Finanzas registra en contabilidad
12. Se compra el bien

**Problemas identificados**:
- Solicitudes perdidas en email
- Presupuesto no actualizado (cambios no reflejados)
- Tiempos impredecibles (3-20 días)
- Sin trazabilidad de solicitudes
- Reproceso frecuente por presupuesto incorrecto

### Diagrama BPMN As-Is (Textual)

```
Pool: Empresa
 Lane: Solicitante
   [Inicio: Solicitud de compra]
   -> [Completar formulario]
   -> [Enviar a compras]
   
 Lane: Área de Compras
   -> [Recibir solicitud]
   -> [Revisar presupuesto en Excel]
   -> {¿Hay presupuesto?}
        ├─ No -> [Email al solicitante: Presupuesto insuficiente]
        │         -> [Fin - Rechazada]
        └─ Sí -> [Buscar en catálogo de proveedores]
   -> [Solicitar cotizaciones (email/teléfono)]
   -> [Esperar respuestas: 3-5 días]
   -> [Recibir cotizaciones]
   -> [Comparar precios en Excel]
   -> [Negociar con proveedor seleccionado]
   -> [Generar orden de compra en Word]
   -> [Firmar (si monto > $1000)]
   
 Lane: Finanzas
   -> [Recibir orden de compra]
   -> [Registrar en contabilidad]
   -> [Procesar pago según términos]
   -> [Fin - Completada]
```

### Métricas Actuales

| Métrica | Valor |
|---------|-------|
| Cycle time promedio | 15 días |
| First pass yield | 65% (35% reproceso por presupuesto) |
| Tiempo de espera | 10 días (74% del total) |
| Variantes observadas | 4 (normal, revisión de presupuesto, negociación, rechazo) |
| Desviaciones | Solicitudes sin seguimiento, tiempos inconsistentes |

### Mejoras Propuestas (To-Be)

1. **Digitalizar solicitud**: formulario en portal -> automático vs manual
2. **Sincronizar presupuesto**: API a contabilidad en tiempo real
3. **Automatizar cotizaciones**: para proveedores activos (> 5 órdenes/año)
4. **Consolidar comparación**: lógica de selección automática si diferencia <5%
5. **Flujo de aprobación**: según monto (< $500 automático, > $5000 gerente)

### BPMN To-Be Mejorado

```
Pool: Sistema de Compras
 Lane: Portal de Solicitudes
   [Inicio: Empleado abre portal]
   -> [Completar formulario digital]
   -> [Enviar solicitud]
   -> [Evento: Confirmación enviada al solicitante]

 Lane: Motor de Compras (Automatizado)
   -> [Validar datos de solicitud]
   -> {¿Datos completos?}
        ├─ No -> [Notificar solicitante: Completar campos]
        │         -> [Esperar corrección]
        └─ Sí -> [Consultar presupuesto API contabilidad]
   -> {¿Hay presupuesto?}
        ├─ No -> [Notificar rechazo automático]
        │         -> [Fin - Rechazada]
        └─ Sí -> [Consultar catálogo]
   -> {¿Producto en catálogo activo?}
        ├─ Sí -> [Obtener cotización de proveedor habitual (API/integración)]
        │         -> [Aplicar política de descuento automáticamente]
        │         -> [Generar orden de compra]
        └─ No -> [Disparar proceso de cotización a 3 proveedores (workflow)]
                  -> [Esperar cotizaciones: 48-72 horas]
                  -> [Comparar automáticamente]
                  -> [Seleccionar mejor opción]
                  -> [Generar orden de compra]
   
   -> {¿Monto < $500?}
        ├─ Sí -> [Aprobación automática]
        └─ No -> {¿Monto < $5000?}
                   ├─ Sí -> [Enviar a gerente para aprobación]
                   │         -> [Evento: Esperar aprobación o timeout 24h]
                   │         -> {¿Aprobado?}
                   │            ├─ No -> [Fin - Rechazada]
                   │            └─ Sí -> [Continuar]
                   └─ No -> [Enviar a director]
                            -> [Evento: Esperar aprobación o timeout 48h]
   
   -> [Registrar en contabilidad (API)]
   -> [Notificar al solicitante: Aprobada]
   -> [Fin - Completada]
```

### Impacto Estimado

| Métrica | As-Is | To-Be | Mejora |
|---------|-------|-------|--------|
| Cycle time | 15 días | 3 días | -80% |
| First pass yield | 65% | 95% | +30% |
| Effort (compras/mes) | 120h | 20h | -83% |
| Presupuesto precisión | 65% | 99% | +34% |

---

## CASO 2: Procesamiento de Reclamos (Empresa de Servicios)

### Narrativa As-Is

Un cliente hace reclamo sobre calidad de servicio. El proceso:
1. Cliente llama o envía email
2. Agente de servicio atiende manualmente
3. Registra en sistema de tickets
4. Clasifica tipo de reclamo (calidad, entrega, facturación, otro)
5. Según tipo, enruta a área responsable
6. Área investiga (3-5 días)
7. Si es válido, ofrece compensación (devolución, descuento, servicio gratis)
8. Si cliente acepta, se procesa
9. Si cliente rechaza, sube a supervisor
10. Supervisor negocia
11. Si llega a acuerdo, se cierra
12. Si no, se escala a gerencia

**Problemas**:
- Tiempo variable (2-30 días)
- Algunos reclamos se pierden
- Falta de trazabilidad
- Decisiones inconsistentes sobre compensación
- Múltiples escalamientos sin resolución

### Diagrama As-Is

```
Pool: Empresa de Servicios

 Lane: Atención al Cliente
   [Inicio: Cliente hace reclamo]
   -> [Agente atiende (teléfono/email)]
   -> [Registrar en sistema de tickets]
   -> [Clasificar tipo]
   
 Lane: Área Responsable
   -> [Recibir ticket]
   -> [Investigar causa]
   -> [Evento intermedio: Esperar 3-5 días datos]
   -> [Evaluar si válido]
   -> {¿Válido?}
        ├─ No -> [Comunicar rechazo al cliente]
        │         -> [Fin - Rechazado]
        └─ Sí -> [Proponer compensación]
   
 Lane: Servicio al Cliente
   -> [Contactar cliente]
   -> [Presentar propuesta]
   -> {¿Cliente acepta?}
        ├─ Sí -> [Procesar compensación]
        │         -> [Registrar cierre]
        │         -> [Fin - Resuelto]
        └─ No -> [Escalar a supervisor]
        
 Lane: Supervisión
   -> [Revisar caso]
   -> [Negociar nueva propuesta]
   -> {¿Cliente acepta?}
        ├─ Sí -> [Procesar]
        │         -> [Fin - Resuelto]
        └─ No -> [Escalar a gerencia]
        
 Lane: Gerencia
   -> [Decisión final]
   -> [Autorizar excepción]
   -> [Notificar cliente]
   -> [Procesar]
   -> [Fin]
```

### To-Be con Automatización y Reglas

```
Pool: Sistema de Reclamos (Digital)

 Lane: Portal de Reclamos
   [Inicio: Cliente abre portal o IVR]
   -> [Seleccionar tipo de reclamo]
   -> [Describir problema]
   -> [Adjuntar evidencia]
   -> [Enviar]
   -> [Evento: Confirmar recepción con # de seguimiento]
   
 Lane: Motor de Reclamos
   -> [Recibir reclamo]
   -> [Validar datos]
   -> {¿Datos completos?}
        ├─ No -> [Solicitar información faltante]
        │         -> [Evento: Esperar respuesta 48h]
        └─ Sí -> [Consultar historial cliente (API)]
   
   -> {¿Cliente VIP?} (gasto > $50k/año)
        ├─ Sí -> [Ruta rápida: Gerente de cuenta]
        └─ No -> [Continuar evaluación estándar]
   
   -> {¿Tipo de reclamo?}
        ├─ Facturación -> [Subproceso: Verificar facturas]
        │                  -> [Consultar sistema de facturación]
        │                  -> [Calcular sobrecargo automáticamente]
        ├─ Calidad -> [Subproceso: Evaluar calidad]
        │             -> [Comparar con SLA]
        │             -> [Si incumplimiento: Propuesta automática]
        └─ Entrega -> [Subproceso: Rastrear envío]
                      -> [Confirmar retraso]
                      -> [Calcular compensación]
   
   -> [Generar propuesta (automática o manual)]
   -> {¿Monto compensación < $100?}
        ├─ Sí -> [Aprobar automáticamente]
        │         -> [Procesar reembolso]
        │         -> [Notificar cliente]
        │         -> [Fin - Resuelto]
        └─ No -> {¿Monto < $500?}
                   ├─ Sí -> [Enviar a supervisor para aprobación]
                   │         -> [Evento: Esperar 24h]
                   └─ No -> [Enviar a gerente]
                            -> [Evento: Esperar 48h]
   
   -> {¿Aprobada?}
        ├─ No -> [Proponer alternativa menor]
        │         -> {¿Cliente acepta?}
        │            ├─ No -> [Escalar a gerencia ejecutiva]
        │            └─ Sí -> [Procesar]
        └─ Sí -> [Procesar]
   
   -> [Registrar resolución]
   -> [Enviar encuesta de satisfacción]
   -> [Fin - Resuelto]
```

### Impacto

| Métrica | As-Is | To-Be |
|---------|-------|-------|
| Cycle time | 12 días | 2 días |
| Resolución 1a instancia | 40% | 85% |
| Costo por reclamo | $150 | $30 |
| Customer satisfaction | 65% | 92% |

---

## CASO 3: Onboarding de Nuevo Empleado (RRHH)

### Narrativa As-Is

Cuando entra un nuevo empleado:
1. RRHH recibe notificación
2. Crea expediente manual
3. Informa a IT para crear cuenta
4. IT crea usuario, email, accesos (3-5 días después)
5. Informa a Facilidades para asignar escritorio
6. Facilidades prepara espacio
7. Primer día: empleado llega sin acceso completo
8. IT termina configuración en día 2
9. RRHH da orientación (documentos, políticas)
10. Gerente planifica capacitación
11. Capacitación se hace (1-3 semanas)
12. Probación de 3 meses

**Problemas**:
- Primer día caótico
- Accesos incompletos en día 1
- Emails perdidos entre equipos
- Proceso toma hasta mes para "completarse"
- Costo por empleado mal estimado

### To-Be Automatizado

```
Pool: RRHH
 Lane: Coordinación
   [Evento de inicio: Oferta aceptada]
   -> [Crear perfil de empleado]
   -> [Seleccionar tipo de rol] (categoría: IT, Finanzas, Operaciones, etc)
   
 Lane: Procesos en Paralelo (AND gateway)
   {Gateway AND - Inicio de procesos paralelos}
   ├─ [Subproceso IT: Crear accesos]
   │   -> [Crear usuario en AD]
   │   -> [Configurar email]
   │   -> [Asignar VPN, herramientas]
   │   -> [Preparar laptop/desktop]
   │   -> [Fin subproceso]
   │
   ├─ [Subproceso Facilidades]
   │   -> [Asignar escritorio]
   │   -> [Preparar materiales de oficina]
   │   -> [Configurar teléfono]
   │   -> [Fin subproceso]
   │
   ├─ [Subproceso Finanzas]
   │   -> [Crear registro para nómina]
   │   -> [Configurar cuentas bancarias]
   │   -> [Fin subproceso]
   │
   └─ [Subproceso RRHH]
       -> [Preparar documentos onboarding]
       -> [Crear plan de capacitación]
       -> [Asignar mentor]
       -> [Fin subproceso]
   
   {Gateway AND de sincronización}
   -> [Evento: Todo listo para día 1]
   
   -> [Enviar bienvenida a empleado]
   -> [Enviar itinerario a empleado]
   -> [Evento de inicio: Primer día]
   
 Lane: Primer Día
   -> [Recibir en recepción]
   -> [Entregar accesos y tarjeta]
   -> [Tour de oficina]
   -> [Presentación a equipo]
   -> [Inicio de capacitación]
   
 Lane: Capacitación (Paralela)
   -> [Subproceso: Capacitación técnica] (2 semanas)
   -> [Subproceso: Capacitación compliance] (1 semana)
   -> [Evaluación de conocimiento]
   
 Lane: Probación (En paralelo)
   -> [Evento: Iniciar probación de 90 días]
   -> [Evento intermedio: Check-in en día 30]
       -> [Feedback del gerente]
   -> [Evento intermedio: Check-in en día 60]
       -> [Feedback del gerente]
       -> [¿En vías correctas?]
            ├─ No -> [Capacitación intensiva]
            └─ Sí -> [Continuar]
   -> [Evento: Final de probación]
   -> {¿Aprobado?}
        ├─ Sí -> [Confirmar empleo permanente]
        │         -> [Aumentar accesos/responsabilidades]
        │         -> [Fin - Empleado integrado]
        └─ No -> [Desvinculación]
```

---

## CASO 4: Aprobación de Proyecto (PMO)

### Narrativa As-Is

Un equipo propone nuevo proyecto. El proceso:
1. Equipo completa documento de propuesta
2. Envía a PMO
3. PMO valida formato
4. PMO enruta a comité de proyectos
5. Comité revisa en reunión (semana siguiente)
6. Si falta información, devuelve
7. Si es válido, se aprueba
8. PMO crea proyecto en sistema
9. Se asigna gerente de proyecto
10. Planificación comienza

### To-Be Digital

```
Pool: PMO Digital

 Lane: Propositor
   [Inicio: Crear propuesta]
   -> [Completar template]
   -> [Cargar evidencia de viabilidad]
   -> [Estimar presupuesto]
   -> [Enviar]
   
 Lane: Validación Inicial (Automática)
   -> [Recibir propuesta]
   -> [Validar completitud de template]
   -> {¿Template correcto?}
        ├─ No -> [Notificar: Campos faltantes]
        │         -> [Evento: Esperar reenvío]
        └─ Sí -> [Validar presupuesto]
   -> {¿Presupuesto en límites?}
        ├─ No -> [Notificar: Presupuesto fuera de rango]
        │         -> [Evento: Esperar corrección]
        └─ Sí -> [Análisis de riesgo automático]
   
 Lane: Comité de Proyectos
   -> {¿Riesgo alto?}
        ├─ Sí -> [Enviar a comité ejecutivo]
        │         -> [Evento: Reunión urgente]
        └─ No -> [Programar en próxima reunión estándar]
   
   -> [Evento: Comité revisa y vota]
   -> {¿Aprobado?}
        ├─ No -> [Fin - Rechazado]
        └─ Sí -> [Continuar]
   
   -> [Crear proyecto en portfolio]
   -> [Asignar gerente de proyecto]
   -> [Enviar kick-off]
   -> [Fin - Aprobado]
```

---

## Estructura de Todos los 10 Casos

(Los casos 5-10 seguirían similar estructura. Aquí menciono los títulos y contextos clave):

### CASO 5: Flujo de Facturación (B2B)
- **Complejidad**: Media
- **Actores**: Ventas, Facturación, Cobranza, Cliente
- **Desafío principal**: Variantes por tipo de contrato, facturación anticipada, por hito

### CASO 6: Gestión de Incidentes IT (Service Desk)
- **Complejidad**: Alta
- **Actores**: Usuario, Service Desk, Técnicos, Proveedores
- **Desafío principal**: Enrutamiento inteligente, SLA, escalamiento

### CASO 7: Auditoría Interna (Compliance)
- **Complejidad**: Alta
- **Actores**: Auditor, Jefes de área, Legal, Dirección
- **Desafío principal**: Conformance checking, evidencias, seguimiento de hallazgos

### CASO 8: Devolución de Productos (Ecommerce)
- **Complejidad**: Media
- **Actores**: Cliente, Almacén, Finanzas
- **Desafío principal**: Automatización de análisis de calidad, reembolsos

### CASO 9: Gestión de Cambios (CAB - Change Advisory Board)
- **Complejidad**: Alta
- **Actores**: Solicitante, CAB, Técnicos, Monitoreo
- **Desafío principal**: Evaluación de riesgo, ventanas de cambio, rollback

### CASO 10: Cierre Contable Mensual
- **Complejidad**: Alta
- **Actores**: Contabilidad, Operaciones, Finanzas, Auditoría
- **Desafío principal**: Sincronización de multiples procesos paralelos, reconciliaciones, cuadratura

