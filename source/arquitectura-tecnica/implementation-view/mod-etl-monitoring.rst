.. meta::
 :artefacto: AT_IMPL_MOD_ETL_MONITORING
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_etl_monitoring:

==========================================
Implementation View — MOD_ETL_Monitoring
==========================================

Componentes y paquetes de codigo del modulo de monitoreo ETL.
Cubre seguimiento de ``ETLEjecucion`` (es_exitosa / es_fallida),
reintentos y registro en ``AuditEvent{ETL_RETRY}``.

.. uml::
 :caption: Implementation View MOD_ETL_Monitoring — componentes de monitoreo de pipeline ETL.

 @startuml

 package "MOD_ETL_Monitoring" {
   component "ETLEjecucionView\nETLRetryView" as ETLView <<api>>
   component "ETLEjecucionSerializer" as ETLSerializer <<serializer>>
   component "ETLMonitoringService\nmonitorear ETLEjecucion\nes_exitosa() / es_fallida()\ngestionar reintentos" as ETLService <<service>>
   component "ETLEjecucionRepository\nETLLogRepository" as ETLRepo <<repository>>
   component "ETLEjecucionORM\nETLLogORM" as ETLORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 ETLView --> ETLSerializer : valida
 ETLView --> ETLService : invoca
 ETLService --> ETLRepo : consulta / persiste
 ETLRepo --> ETLORM : mapea
 ETLORM --> AlmacenDatos : SQL

 note right of ETLService
   ETLEjecucion{pipeline_id, estado, registros_procesados,
     registros_fallidos, iniciado_en, finalizado_en}.
   es_exitosa(): estado=COMPLETADO AND registros_fallidos=0.
   es_fallida(): estado=FALLIDO OR registros_fallidos>0.
   AuditEvent{ETL_RETRY} en cada reintento.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/etl-ejecucion`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
