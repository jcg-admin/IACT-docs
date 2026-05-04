.. _uc-log-07-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_technical_metrics" as view_technical_metrics
 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nMetricas" as UC07
 }
 view_technical_metrics --> UC07
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
 component "Apps" as Apps
 component "Exporters" as Exporters
 component "TSDB" as Tsdb
 component "Endpoint" as Endpoint
 Apps --> Exporters
 Exporters --> Tsdb
 Endpoint --> Tsdb
 @enduml

8.4 Tail SSE
============

Identica a UC_LOG_01 SSE.
