.. meta::
 :artefacto: AT_UC_MOD_PIPELINE
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_pipeline:

=============================================
MOD_Pipeline — Gestion del ETL: UC por Modulo
=============================================

MOD_Pipeline — Gestion del ETL
=================================

Supervision, monitoreo y reintento del pipeline ETL IVR. El ETL
transforma los datos del Repositorio IVR a la Base Analitica IVR
via ``sp_etl_maestro``. El registro de ejecuciones vive en ``etl_runs``.

.. uml::
 :caption: Figura 22 — MOD_Pipeline: casos de uso

 @startuml
 left to right direction

 actor "view_pipeline_status" as view_pipeline_status
 actor "view_pipeline_errors" as view_pipeline_errors
 actor "view_data_availability" as view_data_availability
 actor "request_pipeline_retry" as request_pipeline_retry
 actor "APScheduler\n/ Cron" as APScheduler

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nVer Estado ETL\n(etl_runs)" as P01
   usecase "UC_PIP_02\nVer Errores ETL\n(etl_runs.estado=fallido)" as P02
   usecase "UC_PIP_03\nVer Disponibilidad\nde Datos" as P03
   usecase "UC_PIP_04\nReintentar ETL\n(sp_etl_historico)" as P04
   usecase "Ejecutar ETL\nAutomatico\n(sp_etl_maestro)" as AUTO
 }

 view_pipeline_status --> P01
 view_pipeline_errors --> P02
 view_data_availability --> P03
 request_pipeline_retry --> P04
 APScheduler --> AUTO

 P01 ..> P02 : <<extend>>
 P04 ..> P01 : <<include>>
 AUTO ..> P01 : <<extend>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
