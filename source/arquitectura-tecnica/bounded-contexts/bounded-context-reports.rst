.. meta::
 :artefacto: AT_DOMINIO_04_REPORTS
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_reports:

=====================================================
Modelo de Dominio — Bounded Context Reports y Metrics
=====================================================

4.4 Reports & Metrics
---------------------

Cinco clases: ``Report``, ``Metric``, ``ExportJob``,
``ScheduledReport`` y ``SavedView``. Por D-10 (Z.2 decision log) los
distintos tipos de reporte se modelan como instancias de ``Report``
con un atributo ``scope`` enumerado, no como subclases.

.. uml::
 :caption: Bounded context Reports & Metrics — reportes,
           metricas, exportacion asincrona, programacion y
           vistas guardadas.

 @startuml

 class Report {
   + report_id : UUID
   + scope : ReportScope
   + filters : List<Filter>
   + owner_user_id : UUID
   + state : ReportState
   --
   + view()                <<view_reports>>
   + filter()              <<filter_reports>>
   + share()               <<share_report>>
   + export()              <<delega en ExportJob>>
 }

 class Metric {
   + metric_id : UUID
   + name : MetricName
   + formula : String
   + unit : String
   --
   + compute()
   + view()                <<view_dashboard>>
 }

 class ExportJob {
   + job_id : UUID
   + requested_by : UUID
   + report_id : UUID
   + format : ExportFormat
   + state : JobState
   + enqueued_at : DateTime
   + completed_at : DateTime
   + artifact_path : String
   --
   + enqueue()
   + process()
   + complete()
   + fail()
 }

 class ScheduledReport {
   + schedule_id : UUID
   + report_id : UUID
   + owner_user_id : UUID
   + schedule_expression : String   <<cron>>
   + next_run_at : DateTime
   + last_run_at : DateTime
   + state : ScheduleState
   --
   + create()             <<schedule_report>>
   + modify()
   + disable()            <<BR-009>>
 }

 class SavedView {
   + view_id : UUID
   + owner_user_id : UUID
   + report_id : UUID
   + filters_snapshot : List<Filter>
   + name : String
   + state : ViewState
   --
   + save()               <<save_view>>
   + load()
   + deactivate()         <<BR-009>>
 }

 enum ReportScope {
   GENERAL
   TRANSFERENCES
   IVR_MENUS
   UNIQUE_CLIENTS
   AGENTS
   QUEUES
   CAMPAIGNS
 }

 enum ReportState {
   DRAFT
   PUBLISHED
   ARCHIVED
 }
 enum JobState {
   QUEUED
   PROCESSING
   DONE
   FAILED
 }
 enum ScheduleState {
   ACTIVE
   DISABLED
 }
 enum ViewState {
   ACTIVE
   INACTIVE
 }
 enum ExportFormat {
   CSV
   EXCEL
   PDF
 }

 enum MetricName {
   ABANDONMENT_RATE
   AVG_WAIT_TIME
   EFFICIENCY_INDEX
   ANSWERED_RATE
 }

 Report "1" *-- "1..*" Metric            : compone
 Report "1" -- "0..*" ExportJob
 Report "1" -- "0..*" ScheduledReport
 Report "1" -- "0..*" SavedView
 Report -- ReportScope
 ExportJob -- ExportFormat
 ExportJob -- JobState
 Metric -- MetricName

 note right of ExportJob
   CNST-019 v3.0.0: cola asincrona abstracta.
   CNST-020 v3.0.0: throttling abstracto.
   BR-011 v2.0.0: limites delegados a CNST.
   Cifras concretas y stack tecnologico viven
   en el ADR de implementacion.
 end note

 note right of Report
   D-10: scope es atributo, no subclase.
   Los siete scope canonicos cubren los
   17 UCs del cluster RPT.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
