8.4 Secuencia con tail SSE
===========================

.. uml::

 @startuml
 actor "view_infrastructure_logs" as view_infrastructure_logs
 participant "InfraLogEndpoint" as Infralogendpoint
 database "InfraLogStore" as Infralogstore

 view_infrastructure_logs -> Infralogendpoint : GET /logs/infra/?host=app&severity=ERROR
 Infralogendpoint -> Infralogendpoint : JWT + RBAC (view_infrastructure_logs)
 alt sin permiso
   Infralogendpoint --> view_infrastructure_logs : 403 Forbidden
 else con permiso
   Infralogendpoint -> Infralogstore : consultar WHERE host=app AND severity=ERROR
   Infralogstore --> Infralogendpoint : entries
   Infralogendpoint --> view_infrastructure_logs : 200 + logs
   opt tail SSE solicitado
     loop nuevas entradas
       Infralogstore -> Infralogendpoint : new entry
       Infralogendpoint -> view_infrastructure_logs : SSE data event
     end
   end
 end
 @enduml
