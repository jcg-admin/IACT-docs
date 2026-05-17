.. meta::
 :artefacto: AT_DM_CLASS_PIPELINE_EXECUTION_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_pipeline_execution_repo:

=====================
PipelineExecutionRepo
=====================

Repositorio CRUD de ``PipelineExecution`` (ejecuciones del Servicio
ETL/Pipeline en la tabla ``pipeline_runs`` de MariaDB). Es el punto
unico de escritura para registrar nuevas ejecuciones (auto-disparadas
por scheduler o manuales por reintento) y de consulta para reportes
operacionales y dashboards de salud.

A diferencia de ``PipelineExecution`` (la entity), este repo expone
queries especializadas: filtros por estado, agregaciones por source,
calculos de lag, throughput y latencia. CNST-007 read-only Analytics —
no se borra ni modifica historial.

.. uml::
 :caption: Clase PipelineExecutionRepo — CRUD + queries de PipelineExecution.

 @startuml

 class PipelineExecutionRepo {
   - storage_backend : StorageBackend
   --
   + create(execution : PipelineExecution) : UUID
   + get_by_id(execution_id : UUID) : PipelineExecution
   + find_by_state(state : ExecutionState) : List<PipelineExecution>
   + find_by_source(source : String, period : Period) : List<PipelineExecution>
   + find_failed(period : Period, filters : Map) : List<PipelineExecution>
   + find_recent(period : Period) : List<PipelineExecution>
   + count_running() : Integer
   + verify_idle() : Boolean
   + last_successful_by_dataset(dataset : String) : DateTime
   + calculate_lag(source : String) : Duration
   + calculate_throughput(period : Period) : Float
 }

 class PipelineExecution

 PipelineExecutionRepo "1" --> "*" PipelineExecution : gestiona

 note bottom of PipelineExecutionRepo
   CNST-007 read-only Analytics.
   BR-009 sin DELETE — registros
   permanecen para auditoria operacional.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que consultan PipelineExecutionRepo:

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index` —
  supervisar Pipeline: jobs/lag/throughput/latency.
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/index` —
  consultar errores: filter state=failed con stack traces.
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/index` —
  disponibilidad de datos: last_successful por dataset.
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
  solicitar reintento: verify_idle + create new execution.

UCs que escriben (registran nuevas ejecuciones):

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
  POST /api/pipeline/retry crea PipelineExecution nueva.

Relaciones
==========

- :doc:`pipeline-execution` — entity gestionada por este repo.
- :doc:`pipeline-log` — logs operacionales del run, escritos por workers.
- :doc:`evaluator-reloader` — dispara nuevos runs (manuales o scheduled).
- :doc:`audit-service` — emite ``PIPELINE_RETRY_REQUESTED`` por escritura.
