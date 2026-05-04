.. _uc-log-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_infrastructure_logs" as view_infrastructure_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nLogs Infraestructura" as UC05
   usecase "Filtrar por\nhosts" as FH
   usecase "Filtrar por\nnivel severity" as FS
   usecase "Tail SSE\n(streaming)" as T
 }
 view_infrastructure_logs --> UC05
 UC05 ..> FH : <<extend>>
 UC05 ..> FS : <<extend>>
 UC05 ..> T : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /logs/infra/;
 :JWT + RBAC (view_infrastructure_logs);
 :Validar filtros (host, severity, range);
 :Consultar InfraLogStore;
 :Aplicar filtros;
 :Sanitizar resultados;
 :200 con entries de infraestructura;
 stop
 @enduml

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

8.4 Secuencia con tail SSE
===========================

.. uml::

 @startuml
 actor "view_infrastructure_logs" as view_infrastructure_logs
 participant "InfraLogEndpoint" as Infralogendpoint
 database "InfraLogStore" as Infralogstore

 view_infrastructure_logs -> Infralogendpoint : GET /logs/infra/?host=app&severity=ERROR
 Infralogendpoint -> Infralogendpoint : JWT + RBAC (view_infrastructure_logs)
 alt sin permiso
   Infralogendpoint --> view_infrastructure_logs : 403 Forbidden
 else con permiso
   Infralogendpoint -> Infralogstore : SELECT WHERE host=app AND severity=ERROR
   Infralogstore --> Infralogendpoint : entries
   Infralogendpoint --> view_infrastructure_logs : 200 + logs
   opt tail SSE solicitado
     loop nuevas entradas
       Infralogstore -> Infralogendpoint : new entry
       Infralogendpoint -> view_infrastructure_logs : SSE data event
     end
   end
 end
 @enduml
