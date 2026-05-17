8.4 Secuencia
=============

.. uml::

 @startuml
 actor "hold_calls" as hold_calls
 participant "Endpoint" as Endpoint
 participant "Telephony" as Telephony
 hold_calls -> Endpoint: POST hold
 Endpoint -> Telephony: hold
 Telephony --> Endpoint: ok
 Endpoint --> hold_calls: 200
 @enduml
