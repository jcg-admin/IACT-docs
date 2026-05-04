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
