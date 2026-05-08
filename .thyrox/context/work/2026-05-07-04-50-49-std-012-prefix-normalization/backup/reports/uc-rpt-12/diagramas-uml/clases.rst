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

