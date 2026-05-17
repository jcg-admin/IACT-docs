.. meta::
 :artefacto: AT_DM_CLASS_PIPELINE_LOG
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Logs
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_pipeline_log:

===========
PipelineLog
===========

Registro de log de una ejecución del ``PipelineService``.
Vinculado a ``PipelineExecution`` vía ``execution_id``.
Política de retención CNST-024.

.. uml::
 :caption: Clase PipelineLog — log de ejecución del pipeline.

 @startuml

 class PipelineLog {
   + log_id : UUID
   + execution_id : UUID
   + level : LogLevel
   + message : String
   + occurred_at : DateTime
   --
   + record()
   + view()                <<view_pipeline_logs>>
 }

 enum LogLevel {
   TRACE
   DEBUG
   INFO
   WARN
   ERROR
   FATAL
 }

 PipelineLog "*" -- "1" LogLevel : has

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/logs/uc-log-04/index`

Relaciones
==========

- Pertenece a una ``PipelineExecution`` (via
  ``execution_id``).
- Asociación con ``LogLevel`` (enum).

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
