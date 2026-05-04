.. _uc-sup-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "barge_in_calls" as barge_in_calls
 rectangle "MOD_Supervision" {
   usecase "UC_SUP_02\nBarge-in" as UC
   usecase "Take over" as TO
 }
 barge_in_calls --> UC
 UC ..> TO : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST barge-in;
 :JWT + RBAC + segmento + reason;
 :Telephony bridge 3-way;
 :Audit CALL_BARGED;
 :200;
 stop
 @enduml

8.3 Modes
=========

.. uml::

 @startuml
 [*] --> active
 active --> takeover : disconnect agent
 active --> ended : leave
 takeover --> ended
 ended --> [*]
 @enduml

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
