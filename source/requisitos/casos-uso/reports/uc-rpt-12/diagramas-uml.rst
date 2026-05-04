.. _uc-rpt-12-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 actor "view_reports" as USRD
 rectangle "MOD_Reports" {
   usecase "UC_RPT_12\nReporte Agentes" as UC12
   usecase "Detalle agente" as DET
 }
 view_reports --> UC12
 USRD --> DET
 UC12 ..> DET : <<extend>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con filtros + period;
 if (JWT?) then (no)
   :401; stop
 endif
 if (RBAC?) then (no)
   :403; stop
 endif
 :Resolver segmento;
 :Cache lookup;
 if (Hit?) then (si)
   :return cached;
   stop
 endif
 :Query AgentDailyStat agregado;
 :Calcular KPIs derivados;
 :Construir summary;
 :Cache write;
 :200;
 stop
 @enduml

8.3 Clases
==========

.. uml::

 @startuml
 class AgentReportService {
   list(filters, period, page)
   detail(agent_id, period)
 }
 class AgentDailyStatRepo {
   aggregate_by_agent(filters, period)
   stream_by_agent(agent_id, period)
 }
 class KPICalculator {
   derive_agent_kpis(stats)
 }
 AgentReportService --> AgentDailyStatRepo
 AgentReportService --> KPICalculator
 @enduml

8.4 Secuencia (detalle)
=======================

.. uml::

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "Service" as Service
 participant "AuditSvc" as Auditsvc
 database "Analytics" as Analytics
 User -> Endpoint: GET /agents/{id}/
 Endpoint -> Endpoint: JWT + view_reports
 Endpoint -> Endpoint: verificar agent_id ∈ segmento
 Endpoint -> Service: detail(agent_id)
 Service -> Analytics: query stats
 Analytics --> Service: rows
 Service --> Endpoint: kpis + trend
 Endpoint -> Auditsvc: emit AGENT_DETAIL_VIEWED
 Endpoint --> User: 200
 @enduml
