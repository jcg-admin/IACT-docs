.. _uc-log-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_etl_logs" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nLogs ETL" as UC02
   usecase "Filtrar\npor trimestre" as FT
   usecase "Filtrar\npor estado" as FE
 }
 USR --> UC02
 UC02 ..> FT : <<extend>>
 UC02 ..> FE : <<extend>>
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
 component "ETLScheduler\n(sp_etl_maestro)" as ETL
 database "etl_runs\n(MariaDB)" as DB
 component "LogEndpoint\n(/logs/etl/)" as EP
 actor "view_etl_logs" as U

 ETL --> DB : INSERT ejecucion
 U --> EP : GET filtros
 EP --> DB : SELECT etl_runs
 DB --> EP : filas
 EP --> U : 200 JSON
 @enduml

8.4 Secuencia de consulta ETL log
==================================

.. uml::

 @startuml
 actor "view_etl_logs" as U
 participant "ETLLogEndpoint" as E
 database "etl_runs\n(MariaDB)" as DB

 U -> E : GET /logs/etl/?trimestre=Q1
 E -> E : JWT + RBAC (view_etl_logs)
 alt sin permiso
   E --> U : 403 Forbidden
 else con permiso
   E -> DB : SELECT * FROM etl_runs WHERE trimestre=Q1
   DB --> E : filas
   E --> U : 200 + lista ejecuciones ETL
 end
 @enduml
