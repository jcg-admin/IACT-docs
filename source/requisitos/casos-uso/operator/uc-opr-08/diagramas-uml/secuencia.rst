8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_own_performance_dashboard" as view_own_performance_dashboard
 participant "Endpoint" as Endpoint
 database "Stats" as Stats
 view_own_performance_dashboard -> Endpoint: GET dashboard
 Endpoint -> Stats: query own
 Stats --> Endpoint: rows
 Endpoint --> view_own_performance_dashboard: 200 + KPIs
 @enduml
