8.4 Secuencia
=============

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 database "Analytics" as Analytics
 User -> Endpoint: GET /campaigns/
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> Analytics: aggregate
 Analytics --> Endpoint: rows
 Endpoint --> User: 200 + items
 @enduml
