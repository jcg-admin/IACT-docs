.. _uc-rpt-12-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_RPT_12 — clases del reporte.

 @startuml

 class AgentReportService {
   + get(filters, period, page) : List
   + detail(agent_id, period) : AgentDetail
 }

 class AgentDailyStatRepo {
   + aggregate_by_agent(filters, period) : List
   + stream_by_agent(agent_id, period) : Stream
 }

 class KPICalculator {
   + derive_agent_kpis(stats) : Map
 }

 AgentReportService --> AgentDailyStatRepo : reads
 AgentReportService --> KPICalculator : computes

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/agent-report-service`.
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`.
