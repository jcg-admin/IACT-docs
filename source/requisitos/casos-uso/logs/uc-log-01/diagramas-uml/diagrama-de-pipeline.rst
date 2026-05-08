.. _uc-log-01-parte-08-diagrama-pipeline:

8.3 Diagrama de pipeline — Ingesta de logs
=============================================

.. uml::
 :caption: UC_LOG_01 — pipeline desde apps hasta LogStore.

 @startuml

 component "Aplicaciones del proyecto" as Apps
 component "Log Shipper" as LogShipper
 component "PII Scanner" as PIIScanner
 database  "LogStore" as LogStore

 Apps --> LogShipper : emit log entries
 LogShipper --> PIIScanner : sanitize PII
 PIIScanner --> LogStore : persist entries

 note bottom of PIIScanner
   Filtra patterns sensibles
   antes de almacenar para
   minimizar exposicion de PII.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/application-log`.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`.
