.. meta::
 :artefacto: ARQ_MOD_004_DIAG_FLUJO_ETL
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/etl-monitoring/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_004_flujo_etl_nocturno:

===================================
Flujo ETL Nocturno — sp_etl_maestro
===================================

.. uml::
 :caption: Secuencia ETL nocturno con sp_etl_maestro sobre Almacen de Datos (CNST-006/008).

 @startuml

 actor "APScheduler\n/ Cron" as Apscheduler
 participant "sp_etl_maestro" as sp_etl_maestro
 database "tbl_historico_detalle\ntbl_historico_clientes\n(Repositorio IVR — solo lectura)" as tbl_historico_detalle
 database "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica — escribible)" as BASE_ANALITICA_DESTINO
 database "etl_runs" as etl_runs
 participant "SupervisionETLEndpoint\n(/api/v1/etl/supervision/)" as Supervisionetlendpoint

 Apscheduler -> sp_etl_maestro : CALL sp_etl_maestro(trimestre)\n(ventana nocturna CNST-006/008)
 sp_etl_maestro -> etl_runs : registrar etl_runs (estado=en_ejecucion)
 sp_etl_maestro -> tbl_historico_detalle : consultar tbl_historico_detalle\n(solo lectura CNST-007)
 tbl_historico_detalle --> sp_etl_maestro : registros IVR del trimestre
 sp_etl_maestro -> BASE_ANALITICA_DESTINO : TRUNCATE + registrar base_ivr_detalle
 sp_etl_maestro -> tbl_historico_detalle : consultar tbl_historico_clientes
 tbl_historico_detalle --> sp_etl_maestro : datos clientes del trimestre
 sp_etl_maestro -> BASE_ANALITICA_DESTINO : TRUNCATE + registrar base_ivr_clientes
 sp_etl_maestro -> etl_runs : actualizar etl_runs SET estado=exitoso

 note over Supervisionetlendpoint
   view_pipeline_status consulta etl_runs.
   No interviene en el proceso sp_etl_maestro.
   Solo observa y reporta estado.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/etl-monitoring/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
