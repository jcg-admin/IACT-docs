.. meta::
 :artefacto: AT_DM_CLASS_SCHEDULED_REPORT_LIST_SERVICE
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

.. _dm_class_scheduled_report_list_service:

==========================
ScheduledReportListService
==========================

Servicio de **lectura** que provee a un usuario la lista
de sus ``ScheduledReport``, su detalle y el historial de
ejecuciones (``ScheduledReportRun``). Aplica filtros de
autorización: un usuario solo puede ver sus propios
schedules salvo que tenga ``view_scheduled_reports_all``.

Es la capa de aplicación entre el endpoint HTTP del UC y
el ``ScheduledReportRepo``: aporta paginación,
autorización y enriquecimiento de la respuesta.

.. uml::
 :caption: Clase ScheduledReportListService — lectura
           autorizada de ScheduledReport y sus runs.

 @startuml

 class ScheduledReportListService {
   - repo : ScheduledReportRepo
   - permission_service : PermissionService
   --
   + list(invoker : User, filters : ScheduledFilters, \
          pagination : Pagination) : PagedList<ScheduledReportSummary>
   + detail(scheduled_id : UUID, invoker : User) : ScheduledReportDetail
   + runs(scheduled_id : UUID, invoker : User, \
          pagination : Pagination) : PagedList<RunSummary>
   - assert_can_view(scheduled : ScheduledReport, invoker : User) : void
 }

 class ScheduledReportSummary {
   + scheduled_id : UUID
   + report_type : ReportType
   + cron_schedule : String
   + last_run_at : DateTime
   + last_run_status : RunStatus
 }

 class ScheduledReportDetail {
   + scheduled : ScheduledReport
   + last_runs : List<RunSummary>
 }

 class RunSummary {
   + run_id : UUID
   + started_at : DateTime
   + finished_at : DateTime
   + status : RunStatus
   + output_url : URL
 }

 class ScheduledReportRepo
 class PermissionService
 class PagedList

 ScheduledReportListService "1" o-- "1" ScheduledReportRepo : reads
 ScheduledReportListService "1" o-- "1" PermissionService : checks
 ScheduledReportListService "1" ..> "0..*" ScheduledReportSummary : returns
 ScheduledReportListService "1" ..> "0..*" ScheduledReportDetail : returns
 ScheduledReportListService "1" ..> "0..*" RunSummary : returns

 note right of ScheduledReportListService
   assert_can_view enforces
   ownership salvo permiso
   view_scheduled_reports_all.
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-08/index` —
  UC principal: ver reportes programados.

Relaciones
==========

- Agregación con ``ScheduledReportRepo`` (lectura).
- Agregación con ``PermissionService`` (autorización).
- Devuelve DTOs ligeros (``Summary``, ``Detail``).
