.. meta::
 :artefacto: AT_DM_CLASS_INFRASTRUCTURE_LOG
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

.. _dm_class_infrastructure_log:

=================
InfrastructureLog
=================

Registro de log de la capa de infraestructura. Captura eventos del
host (servidor, contenedor) con identificacion del origen. Politica
de retencion CNST-024.

.. uml::
 :caption: Clase InfrastructureLog — log de infraestructura del sistema.

 @startuml

 class InfrastructureLog {
   + log_id : UUID
   + host : String
   + level : LogLevel
   + message : String
   + occurred_at : DateTime
   --
   + record()
   + view()                <<view_infrastructure_logs>>
 }

 enum LogLevel {
   TRACE
   DEBUG
   INFO
   WARN
   ERROR
   FATAL
 }

 InfrastructureLog -- LogLevel

 @enduml

.. seealso::

