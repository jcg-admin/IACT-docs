.. meta::
 :artefacto: AT_DESIGN_CLASS_REPORTS
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_reports:

============================================================
Design View — MOD_Reports: Estructura de Clases
============================================================

Modulo de **reportes y KPIs**: agregacion de estadisticas
operativas (agente, cola, campana), KPIs derivados, exportacion
asincrona, programacion de reportes recurrentes.

Es el modulo con mas UCs (16) y mas clases del domain-model.

.. uml::
 :caption: MOD_Reports — clases canonicas y relaciones internas.

 @startuml

 class Report
 class HistoricalReport
 class Bucket
 class AgentDailyStat
 class Comparative
 class ExportJob
 class Metric

 class BaseReportService <<sistema>>
 class AgentReportService <<sistema>>
 class CallerReportService <<sistema>>
 class AbandonmentReportService <<sistema>>
 class IvrNavigationReportService <<sistema>>
 class TransferReportService <<sistema>>
 class ScheduledReportListService <<sistema>>
 class ScheduledReportRepo <<sistema>>
 class AgentDailyStatRepo <<sistema>>
 class KpiCalculator <<sistema>>
 class ExportWorker <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 Report <|-- HistoricalReport
 Report --> Bucket : agrupa por
 HistoricalReport --> AgentDailyStat
 Comparative --> Report : compara N

 BaseReportService <|-- AgentReportService
 BaseReportService <|-- CallerReportService
 BaseReportService <|-- AbandonmentReportService
 BaseReportService <|-- IvrNavigationReportService
 BaseReportService <|-- TransferReportService

 AgentReportService ..> AgentDailyStatRepo
 ScheduledReportListService ..> ScheduledReportRepo
 BaseReportService ..> KpiCalculator : derive KPIs
 KpiCalculator ..> Metric

 ExportJob --> Report : snapshot de
 ExportWorker ..> ExportJob : procesa async

 AuthorizationGuard ..> BaseReportService : verify view_*_report
 BaseReportService ..> AuditService : on generate
 ExportJob ..> AuditService : on complete

 @enduml

----

UCs cubiertos
==============

UC_RPT_01..17 + UC_INC_RPT_01 — dashboard, metricas tiempo real,
exportar reporte, reporte de agentes, colas, campanas,
transferencias, IVR, clientes unicos, programados, etc. Ver
:doc:`/arquitectura-tecnica/use-case-view/reports/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/report`
 - :doc:`/arquitectura-tecnica/domain-model/historical-report`
 - :doc:`/arquitectura-tecnica/domain-model/bucket`
 - :doc:`/arquitectura-tecnica/domain-model/comparative`
 - :doc:`/arquitectura-tecnica/domain-model/export-job`
 - :doc:`/arquitectura-tecnica/domain-model/metric`
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/agent-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/caller-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/abandonment-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/transfer-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report-list-service`
 - :doc:`/arquitectura-tecnica/domain-model/scheduled-report-repo`
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo`
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`
 - :doc:`/arquitectura-tecnica/domain-model/export-worker`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/reports/index`
 - :doc:`/arquitectura-tecnica/design-view/reports/sequence`
 - :doc:`/arquitectura-tecnica/design-view/reports/state`
