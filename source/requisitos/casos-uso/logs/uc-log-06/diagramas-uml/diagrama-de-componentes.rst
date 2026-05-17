.. _uc-log-06-parte-08-diagrama-componentes:

8.4 Diagrama de componentes
============================

.. uml::
 :caption: UC_LOG_06 — componentes del Status Service
           agrupados por capa (Boundary / Domain /
           Infrastructure).

 @startuml

 package "Boundary" {
   component "Servicio de Aplicacion" as SA
 }

 package "Domain" {
   component "StatusService" as StatusService
   component "ServiceHealthChecker" as ServiceHealthChecker
   component "DepHealthChecker" as DepHealthChecker
   component "ETLProbe" as ETLProbe
   component "AlertCounter" as AlertCounter
 }

 package "Infrastructure" {
   component "InfraLogStore" as InfraLogStore
   component "Almacen de Datos" as AlmacenDatos
 }

 SA --> StatusService : query status
 StatusService --> ServiceHealthChecker : check apps
 StatusService --> DepHealthChecker : check deps
 StatusService --> ETLProbe : query summary
 StatusService --> AlertCounter : query active count
 ServiceHealthChecker --> InfraLogStore : reads infra logs
 DepHealthChecker --> AlmacenDatos : ping

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/system-health`.
 - :doc:`/arquitectura-tecnica/domain-model/infra-log-store`.
 - :doc:`/arquitectura-tecnica/domain-model/technical-metric`.
