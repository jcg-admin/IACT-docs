.. meta::
 :artefacto: AT_DESIGN_SEQ_REPORTS
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: reports
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_reports:

============================================================
Design View — MOD_Reports: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Reports: generacion de
``AgentReport`` con KPIs derivados (KpiCalculator) leyendo
estadisticas pre-agregadas de ``AgentDailyStatRepo``, opcion
de export asincrono via ``ExportWorker``.

.. uml::
 :caption: MOD_Reports — generacion de reporte con KPIs derivados.

 @startuml

 actor "view_agent_report" as view_agent_report
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AgentReportService" as AgentReportService <<sistema>>
 actor "AgentDailyStatRepo" as AgentDailyStatRepo <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>
 actor "ExportWorker" as ExportWorker <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 view_agent_report -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> view_agent_report : OK
 deactivate AuthorizationGuard

 view_agent_report -> AgentReportService : generate(period, agent_ids)
 activate AgentReportService

 AgentReportService -> AgentDailyStatRepo : query(period, agent_ids)
 activate AgentDailyStatRepo
 AgentDailyStatRepo --> AgentReportService : List<AgentDailyStat>
 deactivate AgentDailyStatRepo

 AgentReportService -> KpiCalculator : derive_agent_kpis(stats)
 activate KpiCalculator
 KpiCalculator --> AgentReportService : KPISet
 deactivate KpiCalculator

 AgentReportService --> view_agent_report : Report

 alt usuario solicita export
   view_agent_report -> ExportWorker : enqueue(report, format)
   activate ExportWorker
   ExportWorker --> view_agent_report : ExportJob{state=pending}
   deactivate ExportWorker
 end

 AgentReportService -> AuditService : emit(AuditEvent\ntype=report_generated)
 activate AuditService
 AuditService --> AgentReportService : OK
 deactivate AuditService
 deactivate AgentReportService

 note right of KpiCalculator
   Strategy stateless. Centraliza
   formulas (occupancy, AHT, ASA,
   service_level, etc.).
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/class-reports`
 - :doc:`/arquitectura-tecnica/design-view/state-export-job`
 - :doc:`/arquitectura-tecnica/design-view/act-export-async`
 - :doc:`/arquitectura-tecnica/use-case-view/reports/index`
 - :doc:`/arquitectura-tecnica/domain-model/agent-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo`
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`
 - :doc:`/arquitectura-tecnica/domain-model/export-worker`
 - :doc:`/arquitectura-tecnica/domain-model/export-job`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
