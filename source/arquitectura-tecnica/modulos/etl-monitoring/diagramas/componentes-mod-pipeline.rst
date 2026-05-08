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

.. uml::
 :caption: Componentes de MOD_Pipeline y sus dependencias de datos.

 @startuml

 actor "APScheduler" as Apscheduler
 actor "request_pipeline_retry" as request_pipeline_retry

 component "sp_etl_maestro\n(Almacen de Datos SP)" as ARTEFACTO_SP_ETL
 component "SupervisionEndpoint\n(/api/v1/etl/supervision/)" as Supervisionendpoint
 component "ETLScheduler\n(tarea programada)" as PROGRAMADOR_ETL

 database "tbl_historico_detalle\ntbl_historico_clientes\n(Repositorio IVR)" as HISTORICO_IVR
 database "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as BASE_ANALITICA
 database "pipeline_runs\n(registro de ejecuciones)" as TABLA_ETL_RUNS
 database "audit_log\n(PostgreSQL)" as TABLA_AUDIT_LOG

 Apscheduler --> PROGRAMADOR_ETL : disparo automatico
 request_pipeline_retry --> Supervisionendpoint : POST reintento (request_pipeline_retry)
 PROGRAMADOR_ETL --> ARTEFACTO_SP_ETL : CALL sp_etl_maestro
 Supervisionendpoint --> ARTEFACTO_SP_ETL : CALL sp_etl_maestro (reintento)
 ARTEFACTO_SP_ETL --> HISTORICO_IVR : consultar (solo lectura)
 ARTEFACTO_SP_ETL --> BASE_ANALITICA : TRUNCATE + registrar
 ARTEFACTO_SP_ETL --> TABLA_ETL_RUNS : registrar/actualizar ejecucion
 Supervisionendpoint --> TABLA_AUDIT_LOG : registrar auditoria

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/etl-monitoring/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
