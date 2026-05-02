.. _uc-pip-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Supervisor\nde Operaciones" as USR
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_02\nErrores ETL" as UC02
   usecase "Filtrar por trimestre" as FT
   usecase "Filtrar por period" as FP
 }
 USR --> UC02
 UC02 ..> FT : <<extend>>
 UC02 ..> FP : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/etl/errores/ con filtros;
 :JWT + RBAC (view_etl_errors);
 :Validar parametros;
 :Consultar Registro de Ejecuciones (fallidas);
 :200 con lista de ejecuciones fallidas;
 stop
 @enduml

8.3 Clases
==========

.. uml::

 @startuml
 class ErroresETLService
 class ETLEjecucionRepo
 ErroresETLService --> ETLEjecucionRepo
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "Supervisor" as U
 participant "Endpoint" as E
 database "Registro de\nEjecuciones" as R
 U -> E: GET /api/v1/etl/errores/
 E -> E: JWT + RBAC
 E -> R: query estado=fallido
 R --> E: filas con mensaje_error
 E --> U: 200 lista ejecuciones fallidas
 @enduml
