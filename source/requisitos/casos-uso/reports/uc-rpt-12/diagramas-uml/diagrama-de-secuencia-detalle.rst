.. _uc-rpt-12-parte-08-diagrama-secuencia-detalle:

8.4 Diagrama de secuencia — Detalle de agente
================================================

.. uml::
 :caption: UC_RPT_12 — flujo de detalle por agente.

 @startuml

 actor "view_reports" as view_reports
 participant "Servicio de Aplicacion" as SvcAplicacion
 participant "AgentReportService" as AgentReportService
 database   "Base Analitica" as BaseAnalitica
 participant "AuditService" as AuditService

 view_reports -> SvcAplicacion: GET /api/v1/agents/{id}/
 SvcAplicacion -> SvcAplicacion: verificar capability
 SvcAplicacion -> SvcAplicacion: verificar agent_id en segmento del user
 SvcAplicacion -> AgentReportService: detail(agent_id)
 AgentReportService -> BaseAnalitica: query stats
 BaseAnalitica --> AgentReportService: rows
 AgentReportService --> SvcAplicacion: kpis + trend
 SvcAplicacion -> AuditService: emit AGENT_DETAIL_VIEWED
 SvcAplicacion --> view_reports: 200 OK

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
