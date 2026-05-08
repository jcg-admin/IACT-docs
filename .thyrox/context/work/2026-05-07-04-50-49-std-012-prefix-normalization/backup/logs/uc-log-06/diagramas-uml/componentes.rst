8.4 Componentes
===============

.. uml::

 @startuml
 component "Status service" as StatusService
 component "ServiceHealthChecker" as Servicehealthchecker
 component "DepHealthChecker" as Dephealthchecker
 component "ETLProbe" as Etlprobe
 component "AlertCounter" as Alertcounter
 StatusService --> Servicehealthchecker
 StatusService --> Dephealthchecker
 StatusService --> Etlprobe
 StatusService --> Alertcounter
 @enduml
