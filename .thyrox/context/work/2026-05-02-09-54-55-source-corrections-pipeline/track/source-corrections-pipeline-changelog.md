```yml
created_at: 2026-05-02 09:54:55
project: IACT-docs
work_package: 2026-05-02-09-54-55-source-corrections-pipeline
author: NestorMonroy
```

# WP Changelog — source-corrections-pipeline

## Added

- discover/source-corrections-pipeline-analysis.md — gap analysis
  completo entre source/ y la arquitectura real descubierta en el WP
  previo (pipeline-uc-deepening). 6 gaps documentados.
- discover/decisions.md — 11 decisiones autónomas (D-ETL-001..D-ETL-011).
- source/requisitos/casos-uso/reports/uc-inc-rpt-01/ — UC formal
  UC_INC_RPT_01 (Resolver Segmento del Usuario), 6 archivos. Extrae
  comportamiento común de los 17 UCs de reporte (D-ETL-010).

## Changed

**databases/**
- modelo-dual.rst v2.0.0 — corregido: MariaDB tiene rol dual (IVR fuente
  + IVR analítica); PostgreSQL es solo para tablas operacionales Django.
  Eliminado error crítico: PostgreSQL como destino del ETL.
- etl-pipeline.rst v2.0.0 — reescrito: SPs en lugar de Python classes;
  tabla etl_runs (D-ETL-002); management command trigger (D-ETL-003);
  7 sp_rpt_* documentados; patrón TRUNCATE+INSERT explicado.

**arquitectura-tecnica/**
- modelo-dominio-iact.rst — Pipeline ETL bounded context: ETLExecution +
  ETLError eliminados; reemplazados por ETLEjecucion con campos de etl_runs.
- matriz-dependencias-uc-iact.rst — UC_PIP_01..04 y UC_LOG_02: entidades
  y funciones RBAC actualizadas a vocabulario D-ETL-005.
- modulos/vis-reports/componentes.rst — DailyMetrics eliminado; reemplazado
  por patrón cursor.callproc() y tabla de 7 sp_rpt_*.

**normativa/**
- cnst-008-sincronizacion-etl-en-ventana-de-6-a-12-horas.rst — ETLRun
  Django ORM eliminado; reemplazado por query directa sobre etl_runs
  en MariaDB.

**requisitos/reglas-negocio/**
- br-016-tasa-abandono.rst v2.0.0 — implementación concreta de los 3
  tipos de abandono (VACIO/cliente_colgo/SinOpcion_Cabecera); umbrales
  recalibrados a <20%/20-30%/>30% con datos Q3 2025 (D-ETL-006/D-ETL-007).

**requisitos/casos-uso/pipeline/**
- uc-pip-01..04/datos-involucrados.rst — entidades ficticias (PipelineRun,
  ETLError, DatasetMetadata) reemplazadas por ETLEjecucion.
- uc-pip-01..04/implementacion-tecnica.rst — stack-agnostic/Airflow/Prefect
  eliminados; cursor queries sobre etl_runs y sp_etl_historico para retry.
- uc-pip-01..04/actores-precondiciones.rst — actores con nombres de rol;
  schema de respuesta alineado con etl_runs.
- uc-pip-01..04/flujo-principal.rst — pasos actualizados con componentes
  reales (ETLEjecucionRepo, DisparadorETL).
- uc-pip-01..04/diagramas-uml.rst — PlantUML actualizado: estados del enum
  etl_runs (en_ejecucion/exitoso/fallido); clases corregidas; plantuml-
  styles.puml incluido.

**requisitos/casos-uso/reports/**
- uc-rpt-01/datos-involucrados.rst — CallEvent/CallSummary/SegmentDimension
  reemplazados por "Base Analítica IVR".
- uc-rpt-03/datos-involucrados.rst — entidades ficticias reemplazadas.
- uc-rpt-13/datos-involucrados.rst + implementacion-tecnica.rst +
  diagramas-uml.rst — QueueDailyStat → Base Analítica IVR via
  sp_rpt_llamadas_abandonadas.
- uc-rpt-15/datos-involucrados.rst + implementacion-tecnica.rst +
  diagramas-uml.rst — TransferEvent → Base Analítica IVR via
  sp_rpt_centros_transferencia + sp_rpt_centros_xsegmento.
- uc-rpt-16/datos-involucrados.rst + implementacion-tecnica.rst +
  diagramas-uml.rst — IVRSessionEvent → Base Analítica IVR via
  sp_rpt_menu_redirigidos + sp_rpt_menu_centro + sp_rpt_cMENU_ERROR.
- uc-rpt-17/datos-involucrados.rst + implementacion-tecnica.rst +
  diagramas-uml.rst — CallSummary/HLL → Base Analítica IVR via
  sp_rpt_clientes; flujo de anonimización documentado.

**otros (sweep final)**
- uc-log-06/datos-involucrados.rst — PipelineRun → ETLEjecucion.
- analisis-catalogo-modular-iact.rst — ETLExecution + ETLError → ETLEjecucion.
- analisis-dominio.rst — ETLExecution → ETLEjecucion.

## Added (sesión 2)

**arquitectura-tecnica/**
- `arquitectura-sistema.rst` v1.0.0 — Arquitectura general del sistema IACT:
  10 funcionalidades principales, Diagrama General (flujo autenticación→cierre
  de sesión), DFD Nivel 0 (sistema como caja negra), DFD Nivel 1 (10
  sub-procesos + 4 data stores). Actores nombrados por función RBAC en inglés.
- `diagramas-uml-sistema.rst` v2.0.0 — 14 secciones de diagramas UML:
  especificación de actores (funciones RBAC), UC general, clases, actividad
  (flujo principal + sub-actividad auth), máquina de estados (sesión IACT +
  sub-máquinas ETL y Reporte con fork/join), secuencia, comunicación,
  componentes (<<System>> con artifacts), despliegue (multi-cliente).
  Actores: funciones RBAC en inglés (D-UML-001).
- `diagramas-uc-por-modulo.rst` v1.0.0 — 12 diagramas UC de módulo (Figuras
  16-27) + mapa de funciones RBAC (Figura 28). Cubre los 80 UCs del sistema:
  MOD_Auth, MOD_Users, MOD_Access, MOD_Permissions, MOD_Reports, MOD_Alerts,
  MOD_Pipeline, MOD_Audit, MOD_Logs, MOD_Operator, MOD_Supervision, MOD_Caller.
- `index.rst` — nueva sección toctree "Vista general del sistema" con los 3
  archivos anteriores.

## Changed (sesión 2)

**arquitectura-tecnica/**
- `arquitectura-sistema.rst` — Actores "Supervisor de Operaciones" y "Analista
  de Datos" reemplazados por funciones RBAC en inglés (D-UML-001):
  `view_etl_status / view_alerts` y `view_reports / view_dashboard`.

**requisitos/casos-uso/pipeline/uc-pip-01..04/**
- Todas las funciones RBAC del pipeline renombradas de español a inglés
  (D-FUNC-001): `ver_estado_etl` → `view_etl_status`, `ver_errores_etl` →
  `view_etl_errors`, `ver_disponibilidad_datos` → `view_data_availability`,
  `reintentar_etl` → `retry_etl`. Afecta: actores-precondiciones, flujo-
  principal, implementacion-tecnica, diagramas-uml, flujos-alternos, etc.

**arquitectura-tecnica/matriz-dependencias-uc-iact.rst**
- PIP-001..004 funciones renombradas a inglés (D-FUNC-001).

**Decisiones documentadas (discover/decisions.md)**
- D-UML-001: Actores en diagramas UML usan nombres de funciones RBAC (inglés).
- D-MENU-001..D-MENU-005: Arquitectura de menú (UC_PERM_08 ya existe).
- D-MENU-006: UC_PERM_08 cubre Generar Menu Dinamico — sin UC duplicado.
- D-FUNC-001: Renombrar funciones pipeline de español a inglés.

## Status de promoción a CHANGELOG.md raíz

Pendiente — el WP continúa con posibles correcciones adicionales.
Promover al merge a main con bump de versión.

## Added (sesión 3 — continuación)

**arquitectura-tecnica/modulos/**
- `operator/index.rst` — ARQ_MOD_009: 10 funciones OPR-001..010,
  AGR-011. Estado del agente, llamadas, disposición, autogestion.
- `operator/diagramas.rst` — State machine (offline→available→busy→
  hold→on_break), secuencia llamada entrante con JWT+RBAC, componentes.
- `supervision/index.rst` — ARQ_MOD_010: 3 funciones SUP-001..003,
  AGR-012. Compliance tone obligatorio en barge-in.
- `supervision/diagramas.rst` — Secuencia monitor_live_calls, state
  canal_agente_cliente→supervision_activa, componentes.
- `caller/index.rst` — ARQ_MOD_011: Caller externo, sin RBAC. PBX→IVR.
- `caller/diagramas.rst` — Activity caller flow (dial→CSAT), componentes
  PBX→tbl_historico_*→ETL→base_ivr_*→AlertEvaluator.

## Changed (sesión 3)

**source/ — corrección masiva nombres de función RBAC (D-DIAG-001)**
- 62 colon-prefix actor declarations corregidas (`actor ":fn"` →
  `actor "fn"`) en diagramas-uc-por-modulo.rst y diagramas-uml-sistema.rst.
- 280 nombres de función incorrectos corregidos en ~80 archivos de
  diagrama RST (view_etl_status→view_pipeline_status, retry_etl→
  request_pipeline_retry, acknowledge_alerts→acknowledge_alert, etc.).
- 148 nombres de función incorrectos corregidos en 110 archivos no-
  diagrama RST (export_reports→export_csv, schedule_reports→
  schedule_report, view_agent_reports→view_reports, etc.).
- 51 instancias de doble sustitución corregidas en 29 archivos
  (search_audit_log_log→search_audit_log, export_audit_log_log→
  export_audit_log) — D-DIAG-002.

**RBAC v5.5.0 — actualización de conteos (D-RBAC-001)**
- 74 funciones (era 42/61/43), 12 grupos (era 10), 11 módulos (era 8/9).
- Archivos actualizados: implementacion.rst, catalogo-funciones.rst,
  grupos-funciones.rst, diagramas.rst, modelo-datos.rst, resumen.rst,
  raci-modulo.rst, mapeo-uc.rst, sod.rst, convenciones.rst,
  base-cognitiva (13 archivos), normativa/restricciones (2), normativa/
  gobernanza (2), backend ADRs (2), requisitos (4), modelo-dominio-iact.

**arquitectura-tecnica/modulos/index.rst**
- "8 modulos funcionales" → "11 modulos funcionales"
- Añadidas filas ARQ_MOD_009, ARQ_MOD_010, ARQ_MOD_011 con conteo de UCs.
- toctree extendido: operator/index, supervision/index, caller/index.

**arquitectura-tecnica/matriz-dependencias-uc-iact.rst**
- 61 UCs → 80 UCs en 12 clusters (D-UC-001).
- Criticality: 9C+34A+24M+13B=80 (era 8C+27A+18M+8B=61).
- Nuevas secciones 2.10 OPR (10 UCs), 2.11 SUP (3 UCs), 2.12 CLI (5 UCs).
- Verification table extendida con OPR/SUP/CLI y totales correctos.
- Transversal deps: T-01/T-02=78/80, T-03=39/80, raíces=23.

**Decisiones documentadas (discover/decisions.md)**
- D-RBAC-001: RBAC v5.5.0 con 74 funciones y 12 grupos.
- D-RBAC-002: Tres nuevos módulos ARQ_MOD_009/010/011.
- D-DIAG-001: Regla actores en UML = nombres exactos de función RBAC.
- D-DIAG-002: Bug de doble sustitución documentado como patrón a evitar.
- D-UC-001: Catálogo IACT: 80 UCs en 12 clusters.

## Added (sesión 4)

**arquitectura-tecnica/uc/ — Vista 4+1 Kruchten (80 archivos)**
- `index.rst` — índice de la vista arquitectónica UC con tabla del
  modelo 4+1 (variante 5+1) y toctree de los 80 UCs por módulo.
  Enlazado en `arquitectura-tecnica/index.rst`.
- `uc-auth-01..05.rst` — 5 UCs MOD_Auth
- `uc-usr-01..04.rst` — 4 UCs MOD_Users
- `uc-acc-01..05, 08, 09.rst` — 7 UCs MOD_Access
- `uc-perm-01..10.rst` — 10 UCs MOD_Permissions
- `uc-inc-rpt-01.rst` + `uc-rpt-01..04, 07..17.rst` — 16 UCs MOD_Reports
- `uc-alr-01..05.rst` — 5 UCs MOD_Alerts
- `uc-pip-01..04.rst` — 4 UCs MOD_Pipeline
- `uc-aud-01..04.rst` — 4 UCs MOD_Audit
- `uc-log-01..07.rst` — 7 UCs MOD_Logs
- `uc-opr-01..10.rst` — 10 UCs MOD_Operator
- `uc-sup-01..03.rst` — 3 UCs MOD_Supervision
- `uc-cli-01..05.rst` — 5 UCs MOD_Caller

  Cada archivo documenta el UC con 6 vistas arquitectónicas:
  1. Domain Model — clase conceptual + relaciones
  2. Design View — secuencia flujo principal
  3. Implementation View — componentes y paquetes
  4. Use Case View — actores RBAC + relaciones
  5. Process View — diagrama de actividades
  6. Deployment View — nodos físicos

  Convenciones aplicadas:
  - Actores = nombres exactos de función RBAC (D-DIAG-001)
  - Sin alias de una sola letra (regla clean code UML_07/UML_09)
  - Alias descriptivos cuando se necesitan (e.g. `as Frontend`)

## Decisiones documentadas (sesión 4)

- **D-UC-002**: Vista arquitectónica 4+1 (5+1) es un archivo por UC,
  separado de la especificación en `requisitos/casos-uso/`. El archivo
  arquitectónico cubre las 6 perspectivas Kruchten; el archivo de
  requisitos documenta el comportamiento funcional.
- **D-DIAG-003**: Aliases en PlantUML deben ser palabras descriptivas,
  nunca letras únicas (e.g. `as U`, `as A`). Regla extraída de
  UML_07/UML_09 en `base-cognitiva/_uml/`.

## Sesión 5 — ETL/ETLEjecucion fixes (2026-05-04)

### Changed
- `source/arquitectura-tecnica/modulos/etl-monitoring/componentes.rst` —
  Reescritura completa: reemplazado modelo Django ORM `ETLExecution`
  ficticio con arquitectura real: tabla `etl_runs` MariaDB (SQL CREATE
  TABLE) + clase `ETLEjecucionRepo` (cursor.execute/callproc). Añadidos
  endpoints API_004 (GET executions/availability, POST retry).
- `source/arquitectura-tecnica/modelo-dominio-iact.rst` —
  Dos correcciones: `ETLExecution` → `ETLEjecucion` (PascalCase español
  coherente con el dominio). Línea tabla de entidades y ejemplo naming.

## Sesión 5 (continuación) — MOD_Operator + RPT/UC stale count fixes (2026-05-04)

### Changed
- `source/arquitectura-tecnica/rbac/modelo-rbac-iact/arquitectura.rst` —
  Sección "Distribución de 73 Funciones" → "74 Funciones"; MOD_Operator
  9 → 10; total 73 → 74; porcentajes recalculados con base 74.
- `source/arquitectura-tecnica/rbac/modelo-rbac-iact/catalogo-funciones.rst` —
  Encabezado "3.9 MOD_Operator (9 funciones)" → "(10 funciones)".
- `source/arquitectura-tecnica/rbac/modelo-rbac-iact/index.rst` —
  "version 5.4.0" → "v5.5.0" en texto descriptivo; MOD_Operator
  9 → 10; total 73 → 74.
- `source/requisitos/reglas-negocio/br-018-indice-eficiencia.rst` —
  "UC_RPT_06" → "UC_RPT_04" en UC Relacionados (UC_RPT_05/06 consolidados
  en UC_RPT_04 per anti-patrón Larman, adr-gob-009).
- `source/requisitos/_metodologia-aplicacion/casos-uso-especificacion.rst` —
  Ejemplo extensión UC: "UC_RPT_05 (extiende con orden)" → "UC_RPT_10
  (extiende con vista guardada)" (UC_RPT_05 ya no existe).
