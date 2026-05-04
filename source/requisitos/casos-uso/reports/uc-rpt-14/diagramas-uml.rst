.. _uc-rpt-14-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_RPT_14\nReporte Campanas" as UC14
   usecase "Detalle" as DET
 }
 view_reports --> UC14
 UC14 ..> DET : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con period + filtros;
 :JWT + RBAC + segmento;
 :Cache lookup;
 :Query CampaignDailyStat;
 :Calcular conversion rate, calls/hour;
 :Cache write;
 :200;
 stop
 @enduml

8.3 Clases
==========

.. uml::

 @startuml
 class CampaignReportService
 class CampaignDailyStatRepo
 class KPICalculator
 CampaignReportService --> CampaignDailyStatRepo
 CampaignReportService --> KPICalculator
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 database "Analytics" as Analytics
 User -> Endpoint: GET /campaigns/
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> Analytics: aggregate
 Analytics --> Endpoint: rows
 Endpoint --> User: 200 + items
 @enduml
