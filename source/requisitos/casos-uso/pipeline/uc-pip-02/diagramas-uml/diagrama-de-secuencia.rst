.. _uc-pip-02-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_PIP_02 — consulta de errores.

 @startuml

 actor "view_pipeline_errors" as view_pipeline_errors
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "PipelineExecutionRepo" as PipelineExecutionRepo

 view_pipeline_errors -> SvcAplicacion: GET /api/v1/etl/errores/
 SvcAplicacion -> SvcAplicacion: verificar capability
 SvcAplicacion -> PipelineExecutionRepo: query state=fallido
 PipelineExecutionRepo --> SvcAplicacion: filas con error_message
 SvcAplicacion --> view_pipeline_errors: 200 con lista

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
