.. _uc-log-02-parte-08-diagrama-componentes-pipeline-log:

8.3 Diagrama de componentes — Pipeline log
=============================================

.. uml::
 :caption: UC_LOG_02 — componentes de logs de ETL.

 @startuml

 component "Disparador ETL\n(sp_etl_maestro)" as DisparadorETL
 database  "pipeline_runs" as pipeline_runs
 component "Servicio de Aplicacion" as SvcAplicacion
 actor     "view_pipeline_logs" as view_pipeline_logs

 DisparadorETL --> pipeline_runs : registrar ejecucion
 view_pipeline_logs --> SvcAplicacion : GET /api/v1/logs/etl/
 SvcAplicacion --> pipeline_runs : consultar
 pipeline_runs --> SvcAplicacion : filas
 SvcAplicacion --> view_pipeline_logs : 200 JSON

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
