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
 Repo -> AlmacenDatos: consultar
 DB --> Repo: rows
 Repo --> Endpoint: items
 Endpoint --> User: 200 + items

 @enduml

