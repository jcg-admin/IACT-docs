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

