.. _uc-log-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_etl_logs" as view_etl_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nLogs ETL" as UC02
   usecase "Filtrar\npor trimestre" as FiltrarTrimestre
   usecase "Filtrar\npor estado" as FiltrarEstado
 }
 view_etl_logs --> UC02
 UC02 ..> FiltrarTrimestre : <<extend>>
 UC02 ..> FiltrarEstado : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /logs/etl/;
 :JWT + RBAC (view_etl_logs);
 :Validar filtros (trimestre, estado);
 :Consultar etl_runs en MariaDB;
 :Filtrar por estado si aplica;
 :Sanitizar resultados;
 :200 con lista de ejecuciones ETL;
 stop
 @enduml

8.3 Componentes ETL log
=======================

.. uml::

 @startuml
 component "ETLScheduler\n(sp_etl_maestro)" as Etlscheduler
 database "etl_runs\n(MariaDB)" as etl_runs
 component "LogEndpoint\n(/logs/etl/)" as Logendpoint
 actor "view_etl_logs" as view_etl_logs

 Etlscheduler --> etl_runs : INSERT ejecucion
 view_etl_logs --> Logendpoint : GET filtros
 Logendpoint --> etl_runs : SELECT etl_runs
 etl_runs --> Logendpoint : filas
 Logendpoint --> view_etl_logs : 200 JSON
 @enduml

8.4 Secuencia de consulta ETL log
==================================

.. uml::

 @startuml
 actor "view_etl_logs" as view_etl_logs
 participant "ETLLogEndpoint" as Etllogendpoint
 database "etl_runs\n(MariaDB)" as etl_runs

 view_etl_logs -> Etllogendpoint : GET /logs/etl/?trimestre=Q1
 Etllogendpoint -> Etllogendpoint : JWT + RBAC (view_etl_logs)
 alt sin permiso
   Etllogendpoint --> view_etl_logs : 403 Forbidden
 else con permiso
   Etllogendpoint -> etl_runs : SELECT * FROM etl_runs WHERE trimestre=Q1
   etl_runs --> Etllogendpoint : filas
   Etllogendpoint --> view_etl_logs : 200 + lista ejecuciones ETL
 end
 @enduml
