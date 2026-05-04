.. _uc-pip-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_pipeline_errors" as view_pipeline_errors
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_02\nErrores ETL" as UC02
   usecase "Filtrar por trimestre" as FiltrarPorTrimestre
   usecase "Filtrar por period" as FiltrarPorPeriod
 }
 view_pipeline_errors --> UC02
 UC02 ..> FiltrarPorTrimestre : <<extend>>
 UC02 ..> FiltrarPorPeriod : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/etl/errores/ con filtros;
 :JWT + RBAC (view_pipeline_errors);
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
 actor "view_pipeline_errors" as view_pipeline_errors
 participant "Endpoint" as Endpoint
 database "Registro de\nEjecuciones" as RegistroDe
 view_pipeline_errors -> Endpoint: GET /api/v1/etl/errores/
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> RegistroDe: query estado=fallido
 RegistroDe --> Endpoint: filas con mensaje_error
 Endpoint --> view_pipeline_errors: 200 lista ejecuciones fallidas
 @enduml
