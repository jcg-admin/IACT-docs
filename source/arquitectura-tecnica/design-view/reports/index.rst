.. meta::
 :artefacto: AT_DESIGN_MOD_REPORTS
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_reports:

============================================================
Design View — MOD_Reports: Vista de Diseño
============================================================

Caja del modulo **MOD_Reports** (dashboards, reportes
historicos, vistas guardadas, programadas y exportes
asincronos). Cubre la jerarquia de servicios de reportes
(Base + 5 especializados), la persistencia de
configuraciones de usuario (``SavedView``), la programacion
de reportes recurrentes (``ScheduledReport``) y el ciclo
asincrono de export jobs.

Materializa los UCs UC_RPT_01..17 + UC_INC_RPT_01
documentados en
:doc:`/arquitectura-tecnica/use-case-view/reports/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Reports — Report + ServiciosEspecializados +
           SavedView + ExportJob. Detalle en :doc:`bounded-context`.

 @startuml

 package "MOD_Reports" {
   class Report <<entity>>
   class SavedView <<entity>>
   class ScheduledReport <<entity>>
   class ExportJob <<entity>>
   class ReportTypeRegistry <<service>>
 }

 class Metric <<external>>
 class SegmentResolver <<external>>
 class AuditService <<external>>

 ReportTypeRegistry ..> Report : <<resolve type>>
 Report ..> Metric : <<consume agregadas>>
 SavedView --> Report : <<persiste config>>
 ScheduledReport --> Report : <<programa>>
 ExportJob --> Report : <<exporta async>>

 SegmentResolver ..> Report : <<aplica scope>>
 ExportJob ..> AuditService : <<emite EXPORT_*>>

 note bottom of Report
   FSM ExportJob (pending → ready |
   failed) en :doc:`export-job-lifecycle`.
   Flujo export async en
   :doc:`async-export-flow`.
 end note

 @enduml

Lectura del diagrama
====================

- **5 entidades centrales:** ``Report`` (instancia
  ejecutada), ``SavedView`` (config persistida del usuario),
  ``ScheduledReport`` (programacion periodica),
  ``ExportJob`` (export asincrono), ``ReportTypeRegistry``
  (registry de tipos de reporte renombrado en WP-H desde
  ReportFactory).
- **Servicios especializados:** AgentReportService,
  CallerReportService, AbandonmentReportService,
  IvrNavigationReportService, TransferReportService,
  CampaignReportService — heredan de ``BaseReportService``.
- **Scope:** ``SegmentResolver`` aplica el segmento del
  usuario (BR-012) para limitar las filas visibles.
- **Export async:** ``ExportJob`` orquesta exportes
  pesados; FSM en :doc:`export-job-lifecycle`, flujo en :doc:`async-export-flow`.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/report` — Report.
- :doc:`/arquitectura-tecnica/domain-model/historical-report`
  — HistoricalReport.
- :doc:`/arquitectura-tecnica/domain-model/saved-view` —
  SavedView.
- :doc:`/arquitectura-tecnica/domain-model/scheduled-report` —
  ScheduledReport.
- :doc:`/arquitectura-tecnica/domain-model/scheduled-report-repo`
  — ScheduledReportRepo.
- :doc:`/arquitectura-tecnica/domain-model/export-job` —
  ExportJob.
- :doc:`/arquitectura-tecnica/domain-model/export-worker` —
  ExportWorker.
- :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
  BaseReportService.
- :doc:`/arquitectura-tecnica/domain-model/agent-report-service` —
  AgentReportService.
- :doc:`/arquitectura-tecnica/domain-model/caller-report-service` —
  CallerReportService.
- :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service` —
  IvrNavigationReportService.
- :doc:`/arquitectura-tecnica/domain-model/transfer-report-service` —
  TransferReportService.
- :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
  SegmentResolver.

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Reports

 bounded-context
 interaction-pattern
 export-job-lifecycle
 async-export-flow

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/reports/index`.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/pipeline/index` —
   productor de Metric.
 - :doc:`/arquitectura-tecnica/design-view/permissions/index` —
   resolver de scope (segment).
 - :doc:`/arquitectura-tecnica/design-view/audit/index` —
   consumidor de eventos EXPORT_*.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.
