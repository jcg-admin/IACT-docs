8.4 Secuencia de consulta ETL log
==================================

.. uml::

 @startuml
 actor "view_pipeline_logs" as view_pipeline_logs
 participant "ETLLogEndpoint" as Etllogendpoint
 database "pipeline_runs" as pipeline_runs

 view_pipeline_logs -> Etllogendpoint : GET /logs/etl/?trimestre=Q1
 Etllogendpoint -> Etllogendpoint : JWT + RBAC (view_pipeline_logs)
 alt sin permiso
   Etllogendpoint --> view_pipeline_logs : 403 Forbidden
 else con permiso
   Etllogendpoint -> pipeline_runs : consultar ejecuciones por trimestre
   pipeline_runs --> Etllogendpoint : filas
   Etllogendpoint --> view_pipeline_logs : 200 + lista ejecuciones ETL
 end
 @enduml
