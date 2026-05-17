8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_own_call_history" as view_own_call_history
 participant "Endpoint" as Endpoint
 database "Calls" as Calls
 view_own_call_history -> Endpoint: GET /me/calls
 Endpoint -> Calls: query own
 Calls --> Endpoint: rows
 Endpoint --> view_own_call_history: 200
 @enduml
