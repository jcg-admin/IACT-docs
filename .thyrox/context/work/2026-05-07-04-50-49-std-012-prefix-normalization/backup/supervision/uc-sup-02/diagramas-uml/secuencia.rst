8.4 Secuencia
=============

.. uml::

 @startuml
 actor "barge_in_calls" as barge_in_calls
 participant "Telephony" as Telephony
 actor "answer_inbound_calls" as answer_inbound_calls
 actor "Caller" as Caller
 barge_in_calls -> Telephony: bridge 3way
 Telephony -> answer_inbound_calls: announce
 Telephony -> Caller: announce
 @enduml
