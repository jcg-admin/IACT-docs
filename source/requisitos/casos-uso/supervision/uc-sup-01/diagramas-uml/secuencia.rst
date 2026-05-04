8.4 Secuencia
=============

.. uml::

 @startuml
 actor "monitor_live_calls" as monitor_live_calls
 participant "Endpoint" as Endpoint
 participant "Telephony" as Telephony
 actor "answer_inbound_calls" as answer_inbound_calls
 monitor_live_calls -> Endpoint: POST monitor
 Endpoint -> Telephony: bridge listen
 Telephony -> answer_inbound_calls: tono "monitor on"
 Endpoint --> monitor_live_calls: 200
 @enduml
