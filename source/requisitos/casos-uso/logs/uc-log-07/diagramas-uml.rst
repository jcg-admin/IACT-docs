.. _uc-log-07-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User con funcion\nview_technical_metrics" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nMetricas" as UC07
 }
 USR --> UC07
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con period + filtros;
 :JWT + RBAC;
 :Cache lookup;
 :Query TSDB;
 :Compute percentiles;
 :Cache write;
 :200;
 stop
 @enduml

8.3 Pipeline metricas
=====================

.. uml::

 @startuml
 component "Apps" as A
 component "Exporters" as E
 component "TSDB" as T
 component "Endpoint" as EP
 A --> E
 E --> T
 EP --> T
 @enduml

8.4 Tail SSE
============

Identica a UC_LOG_01 SSE.
