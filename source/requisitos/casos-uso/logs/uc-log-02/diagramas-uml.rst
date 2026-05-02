.. _uc-log-02-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_etl_logs" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nLogs ETL" as UC02
 }
 USR --> UC02
 @enduml

8.2 — Identicos a UC_LOG_01.
8.3 — Identicos a UC_LOG_01.
8.4 — Identicos a UC_LOG_01.
