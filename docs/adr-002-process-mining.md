# ADR 002 - Estrategia de process mining

## Estado

Propuesto

## Fecha

2026-05-12

## Decision

Incluir `process mining` como modulo formal de la plataforma y usar `PM4Py` como motor inicial open source para el MVP tecnico.

La arquitectura tambien debe permitir conectores futuros con plataformas empresariales como `Celonis`, `Apromore`, `SAP Signavio Process Intelligence` o `UiPath Process Mining`, cuando un cliente ya tenga esas herramientas.

## Contexto

El agente levantara procesos por entrevistas y documentos, pero eso no es suficiente para una plataforma avanzada. Un proceso real tambien deja huella en sistemas como ERP, CRM, BPM, mesa de ayuda, core bancario, sistemas de compras, facturacion o logs de aplicaciones.

El modulo de process mining debe permitir comparar:

- lo que las areas dicen que ocurre;
- lo que el BPMN `as-is` representa;
- lo que los datos historicos muestran que ocurre realmente.

## Motor recomendado

### Opcion base: PM4Py

Se elige `PM4Py` porque:

- es una libreria Python de process mining;
- se integra naturalmente con `FastAPI`, `pandas` y el backend del proyecto;
- soporta descubrimiento de procesos desde event logs;
- permite trabajar con BPMN, Petri nets, XES, OCEL y dataframes;
- cubre capacidades como process discovery, conformance checking, variantes, performance mining y object-centric process mining;
- evita dependencia inicial de una suite comercial.

### Opcion empresarial: adaptadores externos

El sistema no debe competir frontalmente con suites empresariales cuando el cliente ya las tenga. En esos casos debe integrarse.

Adaptadores futuros:

- `Celonis`: para clientes con plataforma de execution/process intelligence.
- `Apromore`: para analisis avanzado, BPMN, simulacion y dashboards si se requiere suite especializada.
- `SAP Signavio Process Intelligence`: para ecosistemas SAP.
- `UiPath Process Mining`: para organizaciones orientadas a automatizacion y RPA.

## Capacidades requeridas

El modulo debe cubrir al menos:

1. carga de event logs;
2. normalizacion de datos;
3. descubrimiento automatico de modelo;
4. analisis de variantes;
5. analisis de frecuencia;
6. analisis de performance;
7. deteccion de cuellos de botella;
8. conformance checking contra BPMN aprobado;
9. extraccion de parametros para simulacion;
10. generacion de hallazgos trazables.

## Formato minimo de event log

Para la primera version, el sistema debe aceptar CSV con estas columnas minimas:

```text
case_id
activity
timestamp
```

Columnas recomendadas:

```text
resource
role
org_unit
system
lifecycle
cost
channel
customer_segment
product
amount
```

Formatos futuros:

- `XES`;
- `OCEL`;
- conectores SQL;
- conectores ERP/CRM;
- ingestion desde data lake.

## Flujo de process mining

```text
1. Importar event log
2. Mapear columnas obligatorias
3. Validar calidad del log
4. Descubrir variantes y modelo inicial
5. Comparar contra narrativa as-is
6. Comparar contra BPMN as-is
7. Identificar desviaciones, retrabajos, esperas y cuellos de botella
8. Proponer hallazgos
9. Solicitar revision humana
10. Alimentar analisis de mejora, to-be y simulacion
```

## Relacion con BPMN

El modulo de process mining no reemplaza el modelado BPMN. Lo complementa.

- BPMN captura diseno, reglas, responsabilidades y excepciones conocidas.
- Process mining muestra comportamiento observado en datos.
- La IA debe reconciliar ambos mundos y marcar diferencias.

Ejemplos de hallazgos:

- actividad frecuente que no existe en el BPMN;
- salto de aprobacion;
- reproceso no documentado;
- variante dominante distinta al proceso oficial;
- SLA incumplido en una rama especifica;
- recurso o area que concentra esperas.

## Modelo de datos adicional

Entidades nuevas:

- `EventLog`
- `EventLogColumnMapping`
- `ProcessEvent`
- `ProcessVariant`
- `MiningRun`
- `DiscoveredProcessModel`
- `ConformanceFinding`
- `PerformanceMetric`
- `BottleneckFinding`

## Riesgos

1. `Logs incompletos`: el proceso puede ocurrir parcialmente fuera del sistema.
2. `Case ID mal definido`: sin un identificador de caso correcto, el analisis se distorsiona.
3. `Timestamps de baja calidad`: errores de zona horaria, fechas faltantes o eventos por lote alteran los tiempos.
4. `Actividad demasiado tecnica`: nombres de transacciones no siempre representan actividades de negocio.
5. `Falsa precision`: los numeros pueden parecer exactos aunque el log no represente todo el proceso.

## Mitigaciones

- validar calidad del log antes de analizar;
- pedir revision humana del mapeo de columnas;
- permitir diccionario de equivalencias entre transacciones y actividades de negocio;
- mostrar nivel de confianza por hallazgo;
- no generar recomendaciones sin declarar supuestos.

## Decision de implementacion

Crear un modulo `process_mining` independiente dentro del backend.

Responsabilidades iniciales:

- importar CSV;
- validar columnas;
- calcular variantes;
- calcular tiempos por caso y actividad;
- descubrir un modelo base con `PM4Py`;
- generar hallazgos preliminares;
- preparar datos para el BPMN y la simulacion.

Fuentes revisadas:

- PM4Py documentation: https://processintelligence.solutions/app/static/api/2.7.17/index.html
- PM4Py features: https://processintelligence.solutions/pm4py/features
- Apromore Core: https://github.com/apromore/ApromoreCore
- Celonis conformance documentation: https://docs.celonis.com/en/conformance.html
- UiPath Process Mining documentation: https://docs.uipath.com/process-mining/automation-cloud/latest/user-guide/process-mining
