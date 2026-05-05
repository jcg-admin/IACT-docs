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

