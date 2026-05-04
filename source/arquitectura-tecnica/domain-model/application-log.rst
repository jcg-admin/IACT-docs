.. meta::
 :artefacto: AT_DM_CLASS_APPLICATION_LOG
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

.. _dm_class_application_log:

==============
ApplicationLog
==============

Registro de log de la capa de aplicacion IACT. Trazabilidad de
operaciones del sistema con nivel de severidad ``LogLevel``.
Politica de retencion CNST-024.

.. uml::
 :caption: Clase ApplicationLog — log de aplicacion del sistema IACT.

 @startuml

 class ApplicationLog {
   + log_id : UUID
   + level : LogLevel
   + message : String
   + source_module : String
   + occurred_at : DateTime
   + user_id : UUID
   --
   + record()              <<sistema>>
   + view()                <<view_application_logs>>
   + search()              <<search_logs>>
   + export()              <<export_logs>>
 }

 enum LogLevel {
   TRACE
   DEBUG
   INFO
   WARN
   ERROR
   FATAL
 }

 ApplicationLog -- LogLevel

 note bottom of ApplicationLog
   CNST-024: politica de retencion de logs.
 end note

 @enduml

.. seealso::

