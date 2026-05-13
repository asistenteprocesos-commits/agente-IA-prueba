# Glosario BPM, BPMN y Process Mining (150+ Términos)

## Fundamentos BPM

### BPM
Disciplina de gestion que identifica, modela, analiza, mejora, ejecuta y monitorea procesos de negocio de extremo a extremo. Integra personas, tecnologia, datos y mejora continua.

### Proceso de negocio
Secuencia de actividades logicamente relacionadas que transforman entradas en salidas con valor para el cliente o stakeholder. Tiene inicio, fin, actores, sistemas, reglas y metricas.

### Gestion por procesos
Enfoque organizacional centrado en procesos en lugar de funciones. Requiere vision de extremo a extremo, accountability por dueño de proceso y mejora continua.

### Owner de proceso
Responsable de desempenio, cambios, cumplimiento normativo y mejora del proceso. Tiene autoridad y accountability sobre indicadores.

### Stakeholder
Persona o area con interes, influencia o impacto en el proceso. Puede ser ejecutor, cliente, regulador, proveedor o soporte.

### Trigger
Evento, condicion o seal que inicia la ejecucion de un proceso o actividad. Puede ser externo (cliente, regulacion) o interno (cambio de estado).

## Modelado BPMN

### BPMN
Notacion estandar para representar procesos de negocio mediante eventos, actividades, gateways, flujos, pools, lanes y artefactos. Lenguaje visual entendible por negocio y tecnologia.

### Elemento BPMN
Componente grafico del diagrama con semantica clara: evento, tarea, gateway, pool, lane, artefacto, flujo o objeto de datos.

### Evento
Punto en el proceso que representa inicio, fin, intermedio o excepcion. Tiene trigger (causa) y es pasivo (ocurre sin accion).

### Evento de inicio
Evento que dispara la ejecucion de un proceso. Puede ser semanal, diario, por demanda, por mensaje o condicional.

### Evento de fin
Evento que termina un proceso. Marca cierre de caso con estado (completado, cancelado, escalonado, error).

### Evento intermedio
Evento que ocurre durante la ejecucion del proceso alterando flujo. Usado para esperas, interrupciones, compensaciones o tiempos.

### Tarea (Task)
Actividad atomica que representa trabajo realizado por una persona, sistema o automatizacion. No se subdivide en el modelo.

### Tarea manual
Trabajo realizado por persona sin soporte de sistema. Ej: revision, aprobacion, firma, validacion documental.

### Tarea de usuario
Tarea asignada a una persona a traves de una cola de trabajo o interfaz. Requiere interaccion humana y decision.

### Tarea de servicio
Actividad automatizada invocada por sistema sin intervencion humana. Ej: envio de email, calculo, integracion API.

### Tarea de envio (Send)
Tarea que genera salida hacia afuera del proceso: correo, mensaje, documento, notificacion.

### Tarea de recepcion (Receive)
Tarea que espera llegada de entrada externa: respuesta de cliente, aprobacion, documento, confirmacion.

### Subproceso
Contenedor que agrupa multiples tareas en una unidad logica reutilizable. Puede colapsar o expandirse. Tiene interfaz (entrada/salida).

### Subproceso llamado (Call Activity)
Referencia a otro proceso definido externamente. Permite reutilizacion, versionado y gobierno centralizado.

### Subproceso transacional
Subproceso con logica de compensacion. Si falla, ejecuta el flujo inverso para deshacer cambios (ej: devolucion de pago).

### Subproceso de evento
Subproceso ejecutado en paralelo que puede ser interrumpido por un evento. Util para monitoreo o rutas alternativas.

### Gateway (Compuerta)
Nodo de decision o convergencia que controla flujo basado en condiciones. Divide o une caminos.

### Gateway exclusivo (XOR)
Compuerta donde exactamente una ruta se ejecuta segun condicion. Las demas se descartan. Patrones: decisiones, bifurcaciones condicionales.

### Gateway paralelo (AND)
Compuerta donde todas las rutas se ejecutan simultaneamente. Usado para trabajo paralelo o sincronizacion de varios caminos.

### Gateway inclusivo (OR)
Compuerta donde una o mas rutas se ejecutan segun multiples condiciones independientes. Combinacion de XOR y AND.

### Gateway basado en eventos
Compuerta que espera primero evento externo para determinar ruta. Usado cuando entrada llega asincronica.

### Pool
Contenedor de nivel superior que representa una organizacion, area o sistema. Define responsabilidad y limites del diagrama.

### Lane (Carril)
Subdivision dentro de un pool que representa rol, area, persona o responsable. Clarifica quien hace que actividad.

### Flujo de secuencia (Sequence Flow)
Conexion entre elementos que define orden de ejecucion. Conecta eventos, tareas y gateways.

### Flujo de mensaje (Message Flow)
Conexion entre dos pools que representa comunicacion entre participantes. Muestra quien envía que a quien.

### Flujo condicional
Flujo de secuencia con condicion explicitada. Solo se ejecuta si la condicion es verdadera. Ej: IF monto > 10000 THEN escalacion.

### Asignacion de roles
Asignacion de tarea a una o mas personas, grupos o roles. Define quien puede ejecutar la tarea.

## Modelado As-is y To-be

### As-is
Descripcion del proceso actual, con actividades, actores, sistemas, reglas, datos, excepciones y problemas existentes. Representacion fiel de la realidad.

### To-be
Diseno del proceso futuro propuesto, validado con responsables y sustentado en evidencia. Incorpora mejoras, automatizaciones, cambios de gobernanza.

### Variante de proceso
Ruta alternativa del flujo principal causada por condiciones, excepciones o caracteristicas del caso. Ej: aprobacion normal vs rapida vs escalonada.

### Ruta de excepcion
Camino alternativo activado por error, evento inesperado o condicion de negocio. Ej: cliente rechaza propuesta, vuelve a negociacion.

### Flujo alto (Happy path)
Ruta principal o mas comun del proceso asumiendo condiciones normales sin excepciones. Usado para entender flujo central.

### Caso (Case)
Instancia de ejecucion del proceso. Tiene atributos (ID, cliente, fecha, estado) y recorre todas las tareas segun las condiciones.

### Atributo de caso
Variable asociada a un caso que persiste durante su ejecucion. Ej: monto, cliente, area, prioridad.

### Estado de caso
Condicion actual del caso en el proceso. Ej: en proceso, completado, en espera, escalonado, cancelado.

## Process Mining y Analisis de Datos

### Process mining
Analisis de procesos a partir de event logs para descubrir modelos, comparar conformidad, medir performance y detectar desviaciones.

### Event log (Registro de eventos)
Registro de eventos con caso, actividad, timestamp, usuario y atributos usados para analizar ejecucion real del proceso.

### Evento
Ocurrencia registrada de una actividad con fecha/hora exacta. Tiene: ID caso, actividad, timestamp, usuario, sistema, estado (completado/error/cancelado).

### Trace (Huella)
Secuencia de actividades ejecutadas en un caso individual. Es la "historia" de un caso desde inicio hasta fin.

### Conformance checking
Comparacion entre comportamiento observado en datos y modelo esperado del proceso. Identifica donde la realidad diverge del modelo.

### Desviacion de conformidad
Huella registrada que no coincide con el modelo esperado. Puede indicar excepciones, errores o reglas no documentadas.

### Descubrimiento de procesos
Tecnica que analiza event logs sin modelo previo para generar automaticamente el grafo de proceso que mejor explica los datos.

### Variante de traza
Secuencia unica de actividades observada en los datos. Si hay 10 clientes con ordenes, pueden haber 5-10 variantes diferentes.

### Drift (Desviacion en tiempo)
Cambio en el comportamiento del proceso detectado a lo largo del tiempo. Ej: antes aprobacion en 2 pasos, ahora en 3 pasos desde junio.

### Performance analysis
Analisis de metricas de desempenio: tiempos, volumenes, colas, repeticiones, errores.

## Metricas y Simulacion

### KPI (Indicador clave de desempenio)
Metrica que mide exito del proceso contra objetivo de negocio. Ej: porcentaje de aprobacion en tiempo, costo por caso.

### SLA (Acuerdo de nivel de servicio)
Compromiso medible sobre desempenio. Ej: procesar 90% de casos en 5 dias habiles.

### Cycle time (Tiempo de ciclo)
Tiempo total desde inicio hasta fin de un caso. Incluye tiempo de trabajo + tiempo de espera.

### Processing time (Tiempo de procesamiento)
Tiempo en que la actividad esta realmente en ejecucion, sin incluir esperas o colas.

### Wait time (Tiempo de espera)
Tiempo transcurrido entre fin de actividad y inicio de la siguiente. Acumulacion causa cuellos.

### Queue (Cola)
Acumulacion de casos esperando entrada a una actividad. Indica cuello de botella o capacidad insuficiente.

### Throughput (Capacidad)
Cantidad de casos procesados en periodo de tiempo. Ej: 100 casos por dia.

### Rework (Reproceso)
Actividades repetidas en el mismo caso. Ej: revision falla, vuelve a paso anterior.

### First pass yield (Éxito a primera)
Porcentaje de casos que se completan sin reproceso o excepcion.

### Bottleneck (Cuello de botella)
Punto del flujo donde se acumula espera, capacidad insuficiente o demora relevante. Identifica restriccion del proceso.

### Simulacion de procesos
Tecnica para estimar impacto de cambios en diseño, capacidad, reglas o carga sin implementar en produccion.

### Escenario de simulacion
Conjunto de supuestos (volumenes, tiempos, probabilidades, capacidad) para proyectar impacto futuro.

### Sensibilidad
Analisis de como cambios en variables (tiempos, volumenes, decisiones) afectan resultados (costo, tiempo, calidad).

## Riesgos y Controles

### Riesgo de proceso
Posibilidad de que el proceso no logre sus objetivos o cause dano a stakeholders. Tiene probabilidad e impacto.

### Control
Mecanismo que mitiga riesgo reduciendo probabilidad o impacto. Puede ser preventivo (evita problema) o detective (detecta problema).

### Segregacion de funciones
Principio que requiere que una persona no tenga simultaneamente autoridad sobre: autorizacion, ejecucion, registro y reconciliacion.

### Conformidad normativa (Compliance)
Cumplimiento de regulaciones, leyes, politicas y estandares aplicables al proceso. Ej: GDPR, SOX, normas contables.

### Trazabilidad
Capacidad de rastrear una transaccion desde origen hasta destino, incluyendo quien, cuando, como y por que.

### Auditoria de control
Verificacion periodica de que el control funciona segun diseno. Ej: muestreo de transacciones, revision de logs.

## Transformacion Digital e Innovacion

### Automatizacion
Reemplazo de tareas manuales por procesos tecnicos. RPA: robotica de procesos. Workflow: motores de orquestacion.

### Robotica de procesos (RPA)
Tecnologia que automatiza tareas repetitivas basadas en reglas usando bots software que simulan acciones de usuario.

### Integracion de sistemas
Conexion entre sistemas de informacion para intercambiar datos en tiempo real, eliminando transcripciones manuales.

### Machine learning en procesos
Uso de algoritmos para detectar patrones, predecir resultados o recomendar acciones sin programacion explicita.

### Prescripcion
Recomendacion automatica de proximo paso o accion basada en datos historicos, reglas y objetivos.

### Transformacion digital
Cambio estrategico que aprovecha tecnologia para redisenar procesos, crear valor y cambiar modelo de negocio.

### Mejora continua
Ciclo sistematico de identificar oportunidades, pilotar, validar e implementar cambios incrementales.

### Lean
Metodologia que elimina desperdicios enfocandose en valor para el cliente. Los 8 desperdicios clasicos.

### Six Sigma
Metodologia que reduce variabilidad y defectos mediante analisis estadistico y prueba sistematica de hipotesis.

## Gestion de Cambio y Gobernanza

### Change management (Gestion de cambio)
Proceso estructurado para autorizar, implementar y monitorear cambios en procesos, sistemas o politicas.

### Gestion de configuracion
Mantenimiento de versiones e interdependencias entre artefactos: BPMN, documentacion, reglas, integraciones.

### Governance (Gobernanza)
Marco de toma de decisiones, autoridades y responsabilidades sobre procesos, cambios e inversiones.

### PMO (Oficina de gestion de proyectos)
Unidad que supervisa portafolio de proyectos, asigna recursos y asegura alineamiento con estrategia.

### Versionado
Control de cambios en artefactos. Cada version tiene numero, fecha, autor, descripcion de cambio.

### Release (Despliegue)
Conjunto de cambios agrupados que se implementan simultaneamente con validacion previa.

## Metodologia de Levantamiento y Analisis

### Entrevista estructurada
Sesion sistematica con guia de preguntas abiertas y cerradas para capturar conocimiento del proceso.

### Taller (Workshop)
Sesion colaborativa con multiples stakeholders para validar, complementar o disenar conjuntamente.

### Cuestionario guiado
Instrumento con preguntas ordenadas por topico para levantamiento asincrono de informacion.

### Observacion directa
Acompanamiento en tiempo real del ejecutor para capturar actividades, decisiones, sistemas usados.

### Analisis documental
Revision de registros, formularios, correos, reportes para extraer hechos sobre proceso.

### Focus group
Sesion grupal con expertos en tema especifico para profundizar en problemas o soluciones.

### Narrativa de proceso
Descripcion textual ordenada del flujo: que se hace, quien lo hace, con que, cuando, por que.

### Matriz de hallazgos
Tabla que clasifica problemas encontrados por tipo (desperdicio, cuello, error, oportunidad) con impacto y evidencia.

## Calidad y Validacion

### Validacion de modelo
Revision de que modelo BPMN es exacto, legible, completo y alineado con realidad del proceso.

### Validador de conformidad BPMN
Verificacion de que diagrama cumple reglas de notacion: inicio/fin, semantica de elementos, convenciones.

### Prueba de cobertura
Ejecucion mental de multiples casos a traves del diagrama para asegurar que todas las variantes estan cubiertas.

### Validacion con stakeholder
Presentacion de modelo a ejecutor, jefe y cliente para asegurar representacion fiel.

## Sistemas y Datos

### Sistema de informacion
Aplicativo usado en proceso para capturar, procesar, almacenar o reportar informacion. ERP, CRM, sistema heredado.

### Integracion de datos
Mecanismo para que sistemas compartan informacion sin entrada manual repetida. API, webhooks, ETL.

### Maestro de datos
Datos de referencia que no cambian frecuentemente. Ej: clientes, productos, centros de costo.

### Dato transaccional
Registro de operacion especifica del caso. Ej: fecha de pedido, monto, estado.

### Lineage (Trazabilidad de datos)
Camino que sigue un dato desde origen (captura) hasta destino (reporte, archivo), incluyendo transformaciones.

## Industria Especifica - Finanzas

### Autorizacion de gasto
Control que requiere aprobacion del gasto por autoridad competente antes de ejecutar transaccion.

### Cuadratura de cuentas
Reconciliacion entre registros contables y datos reales (banco, efectivo, inventario).

### Auditoria interna
Evaluacion periodica de controles internos, cumplimiento y eficiencia de procesos financieros.

### Segregacion de tesoreria
En procesamiento de pagos: quien autoriza, quien ejecuta, quien reconcilia deben ser personas diferentes.

## Industria Especifica - RRHH

### Ciclo de vida de empleado
Etapas de relacion empresa-empleado: reclutamiento, onboarding, desarrollo, movimiento, offboarding.

### Flujo de aprobaciones jerarquicas
Proceso donde tarea pasa a escalones superiores segun criterios (monto, area, tipo).

### Notificacion a multiple
Situacion donde actividad tiene multiples destinatarios simultaneamente. Ej: notificar a gerente y a RRHH.

## Antipatrones Comunes

### Cuello de botella por aprobacion
Espera prolongada en actividad de aprobacion. Causa: baja capacidad, falta de criterios claros, escalamiento excesivo.

### Golden path dominante
Un camino ejecuta 95%+ de casos, otros caminos obsoletos o nunca ejecutados. Indica variantes mal mantenidas.

### Falta de eventos finales
Proceso sin evento de cierre clara. Dificulta cierre de ciclo y reconciliacion.

### Regla de negocio no codificada
Decisiones tomadas por "sentido comun" sin criterio formal. Causa inconsistencia y riesgo de error.

### Datos duplicados entre sistemas
Mismo dato mantenido en multiples lugares sin sincronizacion. Causa inconsistencias y conflictos.

### Reproceso sistematico
Cierto porcentaje de casos siempre vuelve a paso anterior. Causa: calidad de entrada, reglas ambiguas.
