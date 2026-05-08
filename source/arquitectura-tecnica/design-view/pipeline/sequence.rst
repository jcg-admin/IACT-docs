.. meta::
 :artefacto: AT_DESIGN_SEQ_PIPELINE
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: pipeline
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_pipeline:

============================================================
Design View — MOD_Pipeline: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Pipeline: ejecucion ETL con
supervision en tiempo real, publicacion de metricas en cache,
manejo de errores y persistencia de la ejecucion.

.. uml::
 :caption: MOD_Pipeline — ejecucion ETL con MetricsCache.

 @startuml

 actor scheduler <<sistema>>
 actor "PipelineExecution" as PipelineExecution <<sistema>>
 actor "MetricsCache" as MetricsCache <<sistema>>
 actor "PipelineExecutionRepo" as PipelineExecutionRepo <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 scheduler -> PipelineExecution : start(job_id)
 activate PipelineExecution

 PipelineExecution -> PipelineExecutionRepo : persist(state=running)
 PipelineExecution -> AuditService : emit(AuditEvent\ntype=etl_start)

 loop por cada batch
   PipelineExecution -> PipelineExecution : extract -> transform -> load
   PipelineExecution -> MetricsCache : update(metric, value)
   activate MetricsCache
   MetricsCache --> PipelineExecution : OK
   deactivate MetricsCache
 end

 alt exito
   PipelineExecution -> PipelineExecutionRepo : persist(state=completed)
   PipelineExecution -> AuditService : emit(AuditEvent\ntype=etl_completed)
 else error
   PipelineExecution -> PipelineExecutionRepo : persist(state=failed, errors)
   PipelineExecution -> AuditService : emit(AuditEvent\ntype=etl_failed)
 end

 deactivate PipelineExecution

 note right of MetricsCache
   Pre-agregacion incremental
   por bucket. Lectura desde
   MOD_Reports en O(1).
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/pipeline/class`
 - :doc:`/arquitectura-tecnica/design-view/pipeline/state`
 - :doc:`/arquitectura-tecnica/design-view/pipeline/activity`
 - :doc:`/arquitectura-tecnica/use-case-view/pipeline/index`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
 - :doc:`/arquitectura-tecnica/domain-model/metric`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
