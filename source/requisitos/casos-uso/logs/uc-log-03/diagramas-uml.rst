.. _uc-log-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User con funcion\nsearch_logs" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_03\nBuscar Logs" as UC03
 }
 USR --> UC03
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST search;
 :JWT + RBAC;
 :Validar query + range;
 :Throttle;
 :FTS search;
 :Sanitize + cap;
 :200;
 stop
 @enduml

8.3 Componentes — identico a UC_AUD_02 FTS.

8.4 Secuencia — identica a UC_AUD_02.
