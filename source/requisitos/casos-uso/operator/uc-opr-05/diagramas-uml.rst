.. _uc-opr-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "transfer_calls" as transfer_calls
 actor "answer_inbound_calls" as answer_inbound_calls
 rectangle "MOD_Operator" {
   usecase "UC_OPR_05\nTransfer" as UC
   usecase "Warm" as W
   usecase "Cold" as C
 }
 transfer_calls --> UC
 UC ..> W : <<extend>>
 UC ..> C : <<extend>>
 W --> answer_inbound_calls
 C --> answer_inbound_calls
 @enduml

8.2 Actividad warm
==================

.. uml::

 @startuml
 start
 :POST transfer warm;
 :Consult B;
 if (B accepts?) then (no)
   :Cancel; stop
 endif
 :Bridge caller-B;
 :Disconnect A;
 :Audit;
 :200;
 stop
 @enduml

8.3 Actividad cold
==================

.. uml::

 @startuml
 start
 :POST transfer cold;
 :Direct bridge B;
 :Disconnect A;
 :Audit;
 :200;
 stop
 @enduml

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
