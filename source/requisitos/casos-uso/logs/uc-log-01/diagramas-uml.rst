.. _uc-log-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_application_logs" as view_application_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nLogs Sistema" as UC01
   usecase "Tail SSE" as TailSse
 }
 view_application_logs --> UC01
 UC01 ..> TailSse : <<extend>>
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
 component "Apps" as Apps
 component "Log shipper" as LogShipper
 component "LogStore" as Logstore
 component "PIIScanner" as Piiscanner
 Apps --> LogShipper
 LogShipper --> Piiscanner
 Piiscanner --> Logstore
 @enduml

8.4 Tail
========

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 queue "LogStore" as LogStore
 User -> Endpoint: GET tail (SSE)
 loop
   LogStore -> Endpoint: new entry
   Endpoint -> User: data
 end
 @enduml
