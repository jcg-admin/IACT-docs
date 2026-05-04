.. _uc-cli-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 actor "CallRouter" as Callrouter
 rectangle "MOD_Caller" {
   usecase "UC_CLI_03\nEsperar cola" as UC
   usecase "UC_CLI_04\nCallback" as CB
 }
 Caller --> UC
 UC --> Callrouter
 UC ..> CB : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Insert QueueEntry;
 :Music on hold;
 repeat
   :Update position;
   if (Wait > X?) then (si)
     :Ofrecer callback;
   endif
 repeat while (no asignado)
 :Bridge agente;
 :Remove QueueEntry;
 stop
 @enduml

8.3 Estado
==========

.. uml::

 @startuml
 [*] --> waiting
 waiting --> served : agente asigna
 waiting --> abandoned : caller cuelga
 waiting --> callback_offered : > X min
 callback_offered --> waiting : declina
 callback_offered --> callback_scheduled : acepta
 served --> [*]
 abandoned --> [*]
 callback_scheduled --> [*]
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "Caller" as Caller
 participant "Queue" as Queue
 participant "Router" as Router
 actor "answer_inbound_calls" as answer_inbound_calls
 Caller -> Queue: enter
 Queue -> Router: notify
 Router -> answer_inbound_calls: offer
 answer_inbound_calls -> Router: answer
 Router -> Queue: dequeue
 Queue -> Caller: bridge
 @enduml
