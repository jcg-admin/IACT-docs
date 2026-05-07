8.4 Secuencia (detalle)
=======================

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "Service" as Service
 participant "AuditSvc" as Auditsvc
 database "Analytics" as Analytics
 User -> Endpoint: GET /agents/{id}/
 Endpoint -> Endpoint: JWT + view_reports
 Endpoint -> Endpoint: verificar agent_id ∈ segmento
 Endpoint -> Service: detail(agent_id)
 Service -> Analytics: query stats
 Analytics --> Service: rows
 Service --> Endpoint: kpis + trend
 Endpoint -> Auditsvc: emit AGENT_DETAIL_VIEWED
 Endpoint --> User: 200
 @enduml
