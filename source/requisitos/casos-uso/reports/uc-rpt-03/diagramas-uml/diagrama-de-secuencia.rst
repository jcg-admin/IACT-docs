8.4 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_RPT_03 — secuencia

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "Cache" as Cache
 database "Analytics" as Analytics

 User -> Endpoint: GET con filtros
 Endpoint -> Endpoint: JWT + RBAC + segmento + validar
 Endpoint -> Cache: get(key)
 Cache --> Endpoint: miss
 par
   Endpoint -> Analytics: aggregate current
 also
   Endpoint -> Analytics: aggregate prior
 end
 Analytics --> Endpoint: rows
 Endpoint -> Endpoint: calcular KPIs + comparative
 Endpoint -> Cache: set
 Endpoint --> User: 200
 @enduml
