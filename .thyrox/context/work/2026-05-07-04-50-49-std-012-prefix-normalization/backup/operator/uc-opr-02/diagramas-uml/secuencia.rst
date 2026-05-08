8.4 Secuencia
=============

.. uml::

 @startuml
 actor "answer_inbound_calls" as answer_inbound_calls
 participant "Frontend" as Frontend
 participant "Router" as Router
 participant "Endpoint" as Endpoint
 participant "Telephony" as Telephony
 Router -> Frontend: offer
 Frontend -> answer_inbound_calls: ring
 answer_inbound_calls -> Frontend: click answer
 Frontend -> Endpoint: POST answer
 Endpoint -> Telephony: bridge
 Telephony --> Endpoint: ok
 Endpoint --> Frontend: 200
 @enduml
