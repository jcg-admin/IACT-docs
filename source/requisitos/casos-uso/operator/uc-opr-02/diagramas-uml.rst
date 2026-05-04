.. _uc-opr-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "answer_inbound_calls" as answer_inbound_calls
 actor "CallRouter" as Callrouter
 rectangle "MOD_Operator" {
   usecase "UC_OPR_02\nAnswer" as UC
 }
 answer_inbound_calls --> UC
 Callrouter --> UC
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Offer ring;
 if (Agente acepta?) then (no)
   :Decline; stop
 endif
 :Bridge;
 :State busy;
 :Audit CALL_ANSWERED;
 :200;
 stop
 @enduml

8.3 Estado de la llamada
========================

.. uml::

 @startuml
 [*] --> queued
 queued --> offered
 offered --> bridged : answer
 offered --> queued : decline
 offered --> abandoned : caller hangup
 bridged --> ended : hangup
 @enduml

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
