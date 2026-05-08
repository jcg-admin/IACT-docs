.. _uc-log-05-parte-08-diagrama-pipeline-infraestructura:

8.3 Diagrama de pipeline — Logs de infraestructura
======================================================

.. uml::
 :caption: UC_LOG_05 — pipeline desde hosts hasta InfraLogStore.

 @startuml

 component "Hosts (app, db, worker)" as Hosts
 component "Log shipper" as LogShipper
 database  "InfraLogStore" as InfraLogStore
 component "Servicio de Aplicacion" as SvcAplicacion
 actor     "view_infrastructure_logs" as view_infrastructure_logs

 Hosts --> LogShipper : stdout / stderr
 LogShipper --> InfraLogStore : entregar structured logs
 view_infrastructure_logs --> SvcAplicacion : GET filtros
 SvcAplicacion --> InfraLogStore : query
 InfraLogStore --> SvcAplicacion : entries
 SvcAplicacion --> view_infrastructure_logs : 200 JSON

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/infrastructure-log`.
