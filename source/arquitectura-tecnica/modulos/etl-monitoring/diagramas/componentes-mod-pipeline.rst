.. meta::
 :artefacto: ARQ_MOD_004_DIAG_COMPONENTES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/etl-monitoring/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_004_componentes_mod_pipeline:

======================================
Diagrama de componentes — MOD_Pipeline
======================================

Diagrama de componentes — MOD_Pipeline
==========================================

.. uml::
 :caption: Componentes de MOD_Pipeline y sus dependencias de datos.

 @startuml

 actor "APScheduler" as Apscheduler
 actor "request_pipeline_retry" as request_pipeline_retry

 component "sp_etl_maestro\n(MariaDB SP)" as ETL_SP
 component "SupervisionEndpoint\n(/api/v1/etl/supervision/)" as Supervisionendpoint
 component "ETLScheduler\n(Django background task)" as SCHED

 database "tbl_historico_detalle\ntbl_historico_clientes\n(Repositorio IVR)" as HIST
 database "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as ANAL
 database "etl_runs\n(registro de ejecuciones)" as RUNS
 database "audit_log\n(PostgreSQL)" as AUDIT

 Apscheduler --> SCHED : disparo automatico
 request_pipeline_retry --> Supervisionendpoint : POST reintento (request_pipeline_retry)
 SCHED --> ETL_SP : CALL sp_etl_maestro
 Supervisionendpoint --> ETL_SP : CALL sp_etl_maestro (reintento)
 ETL_SP --> HIST : SELECT (solo lectura)
 ETL_SP --> ANAL : TRUNCATE + INSERT
 ETL_SP --> RUNS : INSERT/UPDATE ejecucion
 Supervisionendpoint --> AUDIT : INSERT auditoria

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/etl-monitoring/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
