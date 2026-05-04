.. _uc-alr-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_alert_history" as view_alert_history
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_04\nHistorial" as UC04
 }
 view_alert_history --> UC04
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con filtros + period;
 :JWT + RBAC + segmento;
 :Validar range ≤ 1 ano;
 :Cache lookup;
 :Query Alert resolved/closed;
 :Calcular time-to-ack/resolve;
 :Build summary;
 :Cache write;
 :200;
 stop
 @enduml

8.3 Clases
==========

.. uml::

 @startuml
 class AlertHistoryService
 class AlertRepo {
   query_history(filters, period)
 }
 class TimingCalculator {
   compute_ttak, compute_ttar
 }
 AlertHistoryService --> AlertRepo
 AlertHistoryService --> TimingCalculator
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 database "AlertRepo" as Alertrepo
 User -> Endpoint: GET /history
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> Alertrepo: query
 Alertrepo --> Endpoint: rows
 Endpoint --> User: 200 + summary
 @enduml
