8.4 Secuencia
=============

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "FTS" as Fts
 participant "AuditSvc" as Auditsvc
 User -> Endpoint: POST search
 Endpoint -> Endpoint: JWT + RBAC + validar
 Endpoint -> Fts: search query
 Fts --> Endpoint: hits
 Endpoint -> Auditsvc: emit AUDIT_SEARCH_QUERIED
 Endpoint --> User: 200
 @enduml
