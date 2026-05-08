.. meta::
 :artefacto: AT_DESIGN_CLASS_PIPELINE
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_pipeline:

============================================================
Design View — MOD_Pipeline: Estructura de Clases
============================================================

Modulo de **ETL pipeline**: ejecucion de jobs ETL, monitoreo
de errores, cache de metricas pre-agregadas, supervision del
estado del pipeline.

.. uml::
 :caption: MOD_Pipeline — clases canonicas y relaciones internas.

 @startuml

 class PipelineExecution
 class Metric
 class TechnicalMetric
 class PipelineExecutionRepo <<sistema>>
 class MetricsCache <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 PipelineExecution --> Metric : produce
 Metric <|-- TechnicalMetric : especialza

 PipelineExecutionRepo ..> PipelineExecution : persiste
 MetricsCache ..> Metric : cachea agregados

 AuthorizationGuard ..> PipelineExecutionRepo : verify_function

 PipelineExecution ..> AuditService : transitions FSM
 Metric ..> AuditService : on threshold breach

 @enduml

----

UCs cubiertos
==============

UC_PIP_01..04 — supervisar pipeline ETL, consultar errores,
re-ejecutar job, ver metricas tecnicas. Ver
:doc:`/arquitectura-tecnica/use-case-view/pipeline/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
 - :doc:`/arquitectura-tecnica/domain-model/metric`
 - :doc:`/arquitectura-tecnica/domain-model/technical-metric`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/pipeline/index`
 - :doc:`/arquitectura-tecnica/design-view/pipeline/sequence`
 - :doc:`/arquitectura-tecnica/design-view/pipeline/state`
