.. meta::
 :artefacto: AT_PROC_ETL_PIPELINE
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_proc_etl_pipeline:

======================================================
Process View — Concurrencia Pipeline ETL
======================================================

Patron de concurrencia del pipeline ETL: disparo periodico, cola de
ejecuciones, workers paralelos, reintentos y registro de
``ETLEjecucion`` con ``AuditEvent{ETL_RETRY}``.

.. uml::
 :caption: Process View — concurrencia ETL: dispatcher, cola, workers y retry.

 @startuml

 participant DisparadorETL <<scheduler>>
 participant ColaETL       <<queue>>
 participant WorkerETL_1   <<worker>>
 participant WorkerETL_2   <<worker>>
 participant ETLMonitoringService <<service>>
 database    AlmacenDatos  <<postgresql>>
 database    BDOperativa   <<mariadb, readonly>>

 DisparadorETL -> ColaETL : encolar(pipeline_id)\n[disparo periodico]
 activate ColaETL

 ColaETL -> WorkerETL_1 : despachar(pipeline_id_A)
 ColaETL -> WorkerETL_2 : despachar(pipeline_id_B)
 activate WorkerETL_1
 activate WorkerETL_2

 WorkerETL_1 -> BDOperativa : SELECT datos\n<<CNST-007: readonly>>
 BDOperativa --> WorkerETL_1 : registros

 WorkerETL_2 -> BDOperativa : SELECT datos\n<<CNST-007: readonly>>
 BDOperativa --> WorkerETL_2 : registros

 WorkerETL_1 -> AlmacenDatos : INSERT etl_ejecuciones\n{estado=EN_CURSO}
 WorkerETL_2 -> AlmacenDatos : INSERT etl_ejecuciones\n{estado=EN_CURSO}

 WorkerETL_1 -> AlmacenDatos : UPDATE etl_ejecuciones\n{estado=COMPLETADO}
 deactivate WorkerETL_1

 WorkerETL_2 -> AlmacenDatos : UPDATE etl_ejecuciones\n{estado=FALLIDO,\nregistros_fallidos>0}
 deactivate WorkerETL_2
 deactivate ColaETL

 ETLMonitoringService -> AlmacenDatos : SELECT etl_ejecuciones\nWHERE estado=FALLIDO
 AlmacenDatos --> ETLMonitoringService : ETLEjecucion fallida

 ETLMonitoringService -> ColaETL : reencolar(pipeline_id_B)\n[reintento]
 activate ColaETL
 ColaETL -> WorkerETL_1 : despachar(pipeline_id_B)
 activate WorkerETL_1
 WorkerETL_1 -> AlmacenDatos : UPDATE etl_ejecuciones\n{estado=COMPLETADO}
 WorkerETL_1 -> AlmacenDatos : INSERT audit_events\n{event_type:ETL_RETRY}
 deactivate WorkerETL_1
 deactivate ColaETL

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/etl-ejecucion`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
 :doc:`/arquitectura-tecnica/deploy-view/deploy-etl`
