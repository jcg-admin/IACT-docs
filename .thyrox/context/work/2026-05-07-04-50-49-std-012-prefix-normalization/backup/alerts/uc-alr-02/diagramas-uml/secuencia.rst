8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_alerts" as view_alerts
 participant "Frontend" as Frontend
 participant "Endpoint" as Endpoint
 database "AlertRepo" as Alertrepo

 view_alerts -> Frontend: abrir vista
 loop cada 10s
   Frontend -> Endpoint: GET /alerts/active
   Endpoint -> Endpoint: JWT + RBAC
   Endpoint -> Alertrepo: query active
   Alertrepo --> Endpoint: rows
   Endpoint --> Frontend: 200
   Frontend -> view_alerts: actualizar UI
 end
 @enduml
