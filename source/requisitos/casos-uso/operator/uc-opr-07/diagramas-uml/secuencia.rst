8.4 Secuencia
=============

.. uml::

 @startuml
 actor "request_break" as request_break
 participant "Endpoint" as Endpoint
 participant "Policy" as Policy
 request_break -> Endpoint: POST break
 Endpoint -> Policy: check quota
 Policy --> Endpoint: ok
 Endpoint --> request_break: 200
 @enduml
