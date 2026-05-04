.. meta::
 :artefacto: AT_DM_CLASS_ETL_LOG
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_etl_log:

======
ETLLog
======

Registro de log de una ejecucion del Servicio ETL. Vinculado a
``ETLEjecucion`` via ``execution_id``. Politica de retencion CNST-024.

.. uml::
 :caption: Clase ETLLog — log de ejecucion del pipeline ETL.

 @startuml

 class ETLLog {
   + log_id : UUID
   + execution_id : UUID
   + level : LogLevel
   + message : String
   + occurred_at : DateTime
   --
   + record()
   + view()                <<view_etl_logs>>
 }

 enum LogLevel {
   TRACE
   DEBUG
   INFO
   WARN
   ERROR
   FATAL
 }

 ETLLog -- LogLevel

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-logs`
 :doc:`/arquitectura-tecnica/domain-model/etl-ejecucion`
