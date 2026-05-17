.. _uc-log-07-parte-08-diagrama-pipeline-metricas:

8.3 Diagrama de pipeline — Metricas tecnicas
==============================================

.. uml::
 :caption: UC_LOG_07 — pipeline desde Apps hasta TSDB.

 @startuml

 component "Aplicaciones del proyecto" as Apps
 component "Exporters" as Exporters
 database  "TSDB" as TSDB
 component "Servicio de Aplicacion" as SvcAplicacion

 Apps --> Exporters : emit metrics
 Exporters --> TSDB : escribir series
 SvcAplicacion --> TSDB : query period y filtros

 note bottom of TSDB
   Time-series database.
   Optimizada para queries por
   intervalos temporales.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/technical-metric`.
