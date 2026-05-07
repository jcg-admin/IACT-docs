8.3 Flujo de firma
==================

.. uml::

 @startuml
 rectangle "ReporteRaw" as ReporteRaw
 rectangle "Sanitize" as Sanitize
 rectangle "HashSha256" as HashSha256
 rectangle "HMACKMS" as HMACKMS
 rectangle "ReporteFirmado" as ReporteFirmado
 ReporteRaw --> Sanitize
 Sanitize --> HashSha256
 HashSha256 --> HMACKMS
 HMACKMS --> ReporteFirmado
 @enduml

