.. _uc-log-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_infrastructure_logs" as USR
 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nLogs Infraestructura" as UC05
   usecase "Filtrar por\nhosts" as FH
   usecase "Filtrar por\nnivel severity" as FS
   usecase "Tail SSE\n(streaming)" as T
 }
 USR --> UC05
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
 component "Hosts\n(app, db, worker)" as H
 component "fluent-bit\n(shipper)" as FB
 database "InfraLogStore" as ILS
 component "LogEndpoint\n(/logs/infra/)" as EP
 actor "view_infrastructure_logs" as U

 H --> FB : stdout/stderr
 FB --> ILS : entregar structured logs
 U --> EP : GET filtros
 EP --> ILS : query
 ILS --> EP : entries
 EP --> U : 200 JSON
 @enduml

8.4 Secuencia con tail SSE
===========================

.. uml::

 @startuml
 actor "view_infrastructure_logs" as U
 participant "InfraLogEndpoint" as E
 database "InfraLogStore" as ILS

 U -> E : GET /logs/infra/?host=app&severity=ERROR
 E -> E : JWT + RBAC (view_infrastructure_logs)
 alt sin permiso
   E --> U : 403 Forbidden
 else con permiso
   E -> ILS : SELECT WHERE host=app AND severity=ERROR
   ILS --> E : entries
   E --> U : 200 + logs
   opt tail SSE solicitado
     loop nuevas entradas
       ILS -> E : new entry
       E -> U : SSE data event
     end
   end
 end
 @enduml
