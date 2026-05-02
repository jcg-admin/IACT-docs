.. _uc-log-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_application_logs" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nLogs Sistema" as UC01
   usecase "Tail SSE" as T
 }
 USR --> UC01
 UC01 ..> T : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /logs/system/;
 :JWT + RBAC;
 :Validar range;
 :Query LogStore;
 :Sanitize;
 :200;
 stop
 @enduml

8.3 Pipeline
============

.. uml::

 @startuml
 component "Apps" as A
 component "Log shipper" as S
 component "LogStore" as L
 component "PIIScanner" as P
 A --> S
 S --> P
 P --> L
 @enduml

8.4 Tail
========

.. uml::

 @startuml
 actor "User" as U
 participant "Endpoint" as E
 queue "LogStore" as L
 U -> E: GET tail (SSE)
 loop
   L -> E: new entry
   E -> U: data
 end
 @enduml
