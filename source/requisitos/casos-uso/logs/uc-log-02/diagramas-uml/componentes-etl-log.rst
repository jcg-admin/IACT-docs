8.3 Componentes ETL log
=======================

.. uml::

 @startuml
 component "ETLScheduler\n(sp_etl_maestro)" as Etlscheduler
 database "etl_runs" as etl_runs
 component "LogEndpoint\n(/logs/etl/)" as Logendpoint
 actor "view_etl_logs" as view_etl_logs

 Etlscheduler --> etl_runs : registrar ejecucion
 view_etl_logs --> Logendpoint : GET filtros
 Logendpoint --> etl_runs : consultar etl_runs
 etl_runs --> Logendpoint : filas
 Logendpoint --> view_etl_logs : 200 JSON
 @enduml

