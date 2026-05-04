8.4 Secuencia warm
==================

.. uml::

 @startuml
 actor "transfer_calls" as transfer_calls
 participant "Caller" as Caller
 participant "Telephony" as Telephony
 actor "answer_inbound_calls" as answer_inbound_calls
 transfer_calls -> Telephony: consult answer_inbound_calls
 Telephony -> answer_inbound_calls: ring
 answer_inbound_calls -> Telephony: answer
 Telephony -> transfer_calls: bridged with answer_inbound_calls
 transfer_calls -> answer_inbound_calls: presenta caso
 transfer_calls -> Telephony: complete transfer
 Telephony -> Caller: bridge with answer_inbound_calls
 Telephony -> transfer_calls: disconnect
 @enduml
