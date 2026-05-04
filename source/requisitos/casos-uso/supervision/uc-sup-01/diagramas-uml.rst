.. _uc-sup-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "monitor_live_calls" as monitor_live_calls
 actor "answer_inbound_calls" as answer_inbound_calls
 actor "Caller" as Caller
 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitor" as UC
 }
 monitor_live_calls --> UC
 UC --> answer_inbound_calls
 UC --> Caller
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST monitor;
 :JWT + RBAC;
 :Validar segmento;
 if (Reason ok?) then (no)
   :400; stop
 endif
 :Telephony bridge listen;
 :Tono audible al agente;
 :Audit CALL_MONITORED;
 :200;
 stop
 @enduml

8.3 Modes
=========

.. uml::

 @startuml
 [*] --> silent
 silent --> whisper : switch
 whisper --> silent : switch
 silent --> stopped : stop
 whisper --> stopped : stop
 stopped --> [*]
 @enduml

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
