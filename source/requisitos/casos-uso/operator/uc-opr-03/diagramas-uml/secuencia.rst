8.4 Secuencia
=============

.. uml::

 @startuml
 actor "make_outbound_calls" as make_outbound_calls
 participant "Endpoint" as Endpoint
 participant "Telephony" as Telephony
 make_outbound_calls -> Endpoint: POST outbound
 Endpoint -> Endpoint: JWT + RBAC + validar
 Endpoint -> Telephony: dial
 Telephony --> Endpoint: pickup
 Endpoint --> make_outbound_calls: 200
 @enduml
