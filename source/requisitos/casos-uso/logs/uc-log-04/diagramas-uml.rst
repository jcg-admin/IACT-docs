.. _uc-log-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User con funcion\nexport_logs" as USR
 actor "ExportWorker" as W
 actor "Mailbox" as MB
 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExport" as UC04
 }
 USR --> UC04
 UC04 --> W
 W --> MB
 @enduml

8.2-8.4: Identicos a UC_RPT_04.
