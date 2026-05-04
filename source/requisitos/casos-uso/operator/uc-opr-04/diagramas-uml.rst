.. _uc-opr-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "hold_calls" as hold_calls
 rectangle "MOD_Operator" {
   usecase "UC_OPR_04\nHold/Unhold" as UC
 }
 hold_calls --> UC
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST hold;
 :Validar ownership;
 :Telephony.hold;
 :UPDATE session;
 :Audit CALL_HELD;
 :200;
 stop
 @enduml

8.3 Estado de la llamada
========================

.. uml::

 @startuml
 [*] --> bridged
 bridged --> on_hold : hold
 on_hold --> bridged : unhold
 bridged --> ended : hangup
 on_hold --> ended : caller hangup
 ended --> [*]
 @enduml

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
