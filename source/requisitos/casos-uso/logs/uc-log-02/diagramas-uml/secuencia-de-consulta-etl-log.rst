8.4 Secuencia de consulta ETL log
==================================

.. uml::

 @startuml
 actor "view_etl_logs" as view_etl_logs
 participant "ETLLogEndpoint" as Etllogendpoint
 database "etl_runs" as etl_runs

 view_etl_logs -> Etllogendpoint : GET /logs/etl/?trimestre=Q1
 Etllogendpoint -> Etllogendpoint : JWT + RBAC (view_etl_logs)
 alt sin permiso
   Etllogendpoint --> view_etl_logs : 403 Forbidden
 else con permiso
   Etllogendpoint -> etl_runs : consultar ejecuciones por trimestre
   etl_runs --> Etllogendpoint : filas
   Etllogendpoint --> view_etl_logs : 200 + lista ejecuciones ETL
 end
 @enduml
