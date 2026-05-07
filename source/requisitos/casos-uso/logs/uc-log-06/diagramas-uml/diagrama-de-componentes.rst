.. _uc-log-06-parte-08-diagrama-componentes:

8.4 Diagrama de componentes
============================

.. uml::
 :caption: UC_LOG_06 — componentes del Status Service.

 @startuml

 component "StatusService" as StatusService
 component "ServiceHealthChecker" as ServiceHealthChecker
 component "DepHealthChecker" as DepHealthChecker
 component "ETLProbe" as ETLProbe
 component "AlertCounter" as AlertCounter

 StatusService --> ServiceHealthChecker : check apps
 StatusService --> DepHealthChecker : check deps
 StatusService --> ETLProbe : query summary
 StatusService --> AlertCounter : query active count

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/system-health`.
