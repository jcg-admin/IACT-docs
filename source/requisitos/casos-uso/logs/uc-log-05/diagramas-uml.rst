.. _uc-log-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User con funcion\nview_infrastructure_logs" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nLogs Infra" as UC05
 }
 USR --> UC05
 @enduml

8.2 Actividad - identica a UC_LOG_01.
8.3 Pipeline - hosts → fluent-bit → InfraLogStore.
8.4 Tail - identica.
