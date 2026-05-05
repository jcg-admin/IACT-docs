8.3 Componentes Pipeline log
============================

.. uml::

 @startuml
 component "ETLScheduler\n(sp_etl_maestro)" as Etlscheduler
 database "pipeline_runs" as pipeline_runs
 component "LogEndpoint\n(/logs/etl/)" as Logendpoint
 actor "view_pipeline_logs" as view_pipeline_logs

 Etlscheduler --> pipeline_runs : registrar ejecucion
 view_pipeline_logs --> Logendpoint : GET filtros
 Logendpoint --> pipeline_runs : consultar pipeline_runs
 pipeline_runs --> Logendpoint : filas
 Logendpoint --> view_pipeline_logs : 200 JSON
 @enduml

