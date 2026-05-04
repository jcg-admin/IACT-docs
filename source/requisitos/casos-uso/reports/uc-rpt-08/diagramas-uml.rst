.. _uc-rpt-08-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_08 — listar programados

 @startuml
 left to right direction
 actor "view_reports" as view_reports

 rectangle "MOD_Reports" {
   usecase "UC_RPT_08\nList scheduled" as UC08
   usecase "Detalle" as DET
   usecase "Historico runs" as RUNS
 }

 view_reports --> UC08
 UC08 ..> DET : <<extend>>
 UC08 ..> RUNS : <<extend>>
 @enduml

8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_08 — list

 @startuml
 start
 :GET /api/reports/scheduled/;
 if (JWT?) then (no)
   :401; stop
 endif
 if (RBAC?) then (no)
   :403; stop
 endif
 :Query schedules del User (o scope);
 :Aplicar filtros;
 :Paginar;
 :200 OK;
 stop
 @enduml

8.3 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_RPT_08 — flujo

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "Repo" as Repo
 database "AlmacenDatos" as AlmacenDatos

 User -> Endpoint: GET /scheduled/
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> Repo: list(actor_id, filters)
 Repo -> AlmacenDatos: SELECT
 DB --> Repo: rows
 Repo --> Endpoint: items
 Endpoint --> User: 200 + items

 @enduml

8.4 Diagrama de clases
======================

.. uml::
 :caption: Estructura

 @startuml
 class ScheduledReportListService {
   list(actor_id, filters, pagination)
   detail(id, invoker)
   runs(id, invoker, pagination)
 }

 class ScheduledReportRepo {
   list_by_actor(actor_id, filters)
   get(id)
   list_runs(id)
 }

 ScheduledReportListService --> ScheduledReportRepo
 @enduml
