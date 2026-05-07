.. _uc-pip-04-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_PIP_04 — solicitud de reintento.

 @startuml

 actor "request_pipeline_retry" as request_pipeline_retry
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "PipelineExecutionRepo" as PipelineExecutionRepo
 participant "DisparadorETL" as DisparadorETL
 participant "AuditService" as AuditService

 request_pipeline_retry -> SvcAplicacion: POST /api/v1/etl/reintento/
 SvcAplicacion -> SvcAplicacion: verificar capability + validar
 SvcAplicacion -> PipelineExecutionRepo: hay ETL en ejecucion?
 PipelineExecutionRepo --> SvcAplicacion: false
 SvcAplicacion -> PipelineExecutionRepo: registrar (manual=True)
 SvcAplicacion -> DisparadorETL: invocar reproceso
 SvcAplicacion -> AuditService: emit ETL_REINTENTO_SOLICITADO
 SvcAplicacion --> request_pipeline_retry: 202 Accepted con etl_run_id

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
