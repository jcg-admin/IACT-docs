.. meta::
 :artefacto: AT_DM_CLASS_PIPELINE_EXECUTION
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Pipeline
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_pipeline_execution:

=================
PipelineExecution
=================

Registro de una ejecución del ``PipelineService``. Persistida
en la tabla ``pipeline_runs`` del datastore (propiedad IACT).
Los errores no son entidades separadas: el campo
``error_message`` captura el fallo. El scheduler es
infraestructura, no dominio.

.. uml::
 :caption: Clase PipelineExecution — registro de ejecución del
           pipeline de datos.

 @startuml

 class PipelineExecution {
   + id : Integer
   + source_table : String
   + period : String
   + started_at : DateTime
   + finished_at : DateTime
   + status : ExecutionStatus
   + base_records : Integer
   + error_message : String
   + executed_by : String
   --
   + is_successful() : Boolean
   + is_failed() : Boolean
   + duration_seconds() : Integer
 }

 enum ExecutionStatus {
   IN_PROGRESS
   SUCCEEDED
   FAILED
 }

 PipelineExecution "*" -- "1" ExecutionStatus : has

 note right of PipelineExecution
   CNST-033 §3.5: campos snake_case ingles.
   CNST-007: tbl_historico_* solo lectura.
   CNST-008: pipeline en ventana 6-12 horas.
   Persistida en pipeline_runs.
 end note

 @enduml

Operaciones principales
=======================

- ``is_successful()`` — short circuit para
  ``status == SUCCEEDED``.
- ``is_failed()`` — short circuit para
  ``status == FAILED``.
- ``duration_seconds()`` — diferencia entre
  ``finished_at`` y ``started_at`` en segundos. Devuelve
  ``null`` si la ejecución sigue en progreso.

Restricciones aplicables
========================

- **CNST-033** §3.5: campos SQL en ``snake_case``
  inglés, ``*_at`` para datetime.
- **CNST-024**: política de retención.
- **CNST-007**: ventana de lectura de tablas
  históricas.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index`
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index`

Relaciones
==========

- Asociación con ``ExecutionStatus`` (enum).
- Referenciada por ``PipelineLog`` vía ``execution_id``.
