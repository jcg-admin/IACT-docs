.. meta::
 :artefacto: AT_DM_CLASS_SCHEDULED_REPORT_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_scheduled_report_repo:

===================
ScheduledReportRepo
===================

Repositorio CRUD de ``ScheduledReport`` y de sus
``ScheduledReportRun`` (registro histórico de
ejecuciones). Los reportes programados se ejecutan según
``cron_schedule`` por un worker externo
(bounded context Pipeline) que invoca al servicio de
generación correspondiente.

Cada ejecución produce un ``ScheduledReportRun`` con
``status``, ``started_at``, ``finished_at`` y
``output_url`` (resultado descargable). Los runs viejos
se archivan según política de retención.

.. uml::
 :caption: Clase ScheduledReportRepo — CRUD de reportes
           programados y trazabilidad de ejecuciones.

 @startuml

 class ScheduledReportRepo {
   - storage_backend : StorageBackend
   --
   + create(scheduled : ScheduledReport) : UUID
   + update(scheduled_id : UUID, changes : ScheduledReportChanges) : ScheduledReport
   + disable(scheduled_id : UUID, actor_user_id : UUID, reason : String) : ScheduledReport
   + list_by_actor(owner_user_id : UUID, filters : ScheduledFilters) : List<ScheduledReport>
   + get(scheduled_id : UUID) : ScheduledReport
   + list_due(at : DateTime) : List<ScheduledReport>
   + record_run(run : ScheduledReportRun) : UUID
   + list_runs(scheduled_id : UUID) : List<ScheduledReportRun>
 }

 class ScheduledReport {
   + scheduled_id : UUID
   + owner_user_id : UUID
   + report_type : ReportType
   + filters : ReportFilters
   + cron_schedule : String
   + delivery_target : DeliveryTarget
   + status : ScheduledStatus
 }

 class ScheduledReportRun {
   + run_id : UUID
   + scheduled_id : UUID
   + started_at : DateTime
   + finished_at : DateTime
   + status : RunStatus
   + output_url : URL
   + error : String
 }

 enum ScheduledStatus {
   ENABLED
   DISABLED
 }

 enum RunStatus {
   RUNNING
   SUCCEEDED
   FAILED
   SKIPPED
 }

 ScheduledReportRepo ..> ScheduledReport : persists
 ScheduledReportRepo ..> ScheduledReportRun : persists
 ScheduledReport "1" -- "*" ScheduledReportRun : has

 note right of ScheduledReportRepo
   list_due(at) lo consume el worker
   del scheduler para encolar
   ejecuciones pendientes.
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-07/index`
  — programar reporte (``create``).
- :doc:`/requisitos/casos-uso/reports/uc-rpt-08/index`
  — ver reportes programados (``list_by_actor``,
  ``list_runs``).

Relaciones
==========

- Persiste ``ScheduledReport`` y ``ScheduledReportRun``.
- Asociación ``ScheduledReport "1" -- "*"
  ScheduledReportRun``.
- Usado por ``ScheduledReportListService`` (lectura) y
  por el worker del scheduler (escritura ``record_run``).
