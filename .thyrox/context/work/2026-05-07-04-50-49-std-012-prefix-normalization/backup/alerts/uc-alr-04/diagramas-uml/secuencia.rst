8.4 Secuencia
=============

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 database "AlertRepo" as Alertrepo
 User -> Endpoint: GET /history
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> Alertrepo: query
 Alertrepo --> Endpoint: rows
 Endpoint --> User: 200 + summary
 @enduml
