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

## Status de promoción a CHANGELOG.md raíz

Pendiente — el WP continúa con posibles correcciones adicionales.
Promover al merge a main con bump de versión.
