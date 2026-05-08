8.3 Pipeline de infraestructura
================================

.. uml::

 @startuml
 component "Hosts\n(app, db, worker)" as Hosts
 component "fluent-bit\n(shipper)" as FluentBit
 database "InfraLogStore" as Infralogstore
 component "LogEndpoint\n(/logs/infra/)" as Logendpoint
 actor "view_infrastructure_logs" as view_infrastructure_logs

 Hosts --> FluentBit : stdout/stderr
 FluentBit --> Infralogstore : entregar structured logs
 view_infrastructure_logs --> Logendpoint : GET filtros
 Logendpoint --> Infralogstore : query
 Infralogstore --> Logendpoint : entries
 Logendpoint --> view_infrastructure_logs : 200 JSON
 @enduml

