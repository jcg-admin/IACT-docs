.. _uc-log-02-parte-08-diagrama-secuencia-pipeline-log:

8.4 Diagrama de secuencia — Consulta de Pipeline log
======================================================

.. uml::
 :caption: UC_LOG_02 — flujo de request.

 @startuml

 actor "view_pipeline_logs" as view_pipeline_logs
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "pipeline_runs" as pipeline_runs

 view_pipeline_logs -> SvcAplicacion : GET /api/v1/logs/etl/?trimestre=Q1
 SvcAplicacion -> SvcAplicacion : verificar capability
 alt sin permiso
   SvcAplicacion --> view_pipeline_logs : 403 Forbidden
 else con permiso
   SvcAplicacion -> pipeline_runs : consultar por trimestre
   pipeline_runs --> SvcAplicacion : filas
   SvcAplicacion --> view_pipeline_logs : 200 + lista ejecuciones
 end

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
