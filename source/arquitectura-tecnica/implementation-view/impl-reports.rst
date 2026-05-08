.. meta::
 :artefacto: AT_IMPL_MOD_VIS_REPORTS
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_vis_reports:

==========================================
Implementation View — MOD_VisReports
==========================================

Componentes y paquetes de codigo del modulo de visualizacion y reportes.
Cubre ``Report`` con filtros por ``ReportScope``, ``ScheduledReport``,
``SavedView``, ``Metric`` y exportacion via ``ExportJob``.

.. uml::
 :caption: Implementation View MOD_VisReports — componentes de reportes y visualizacion.

 @startuml

 package "MOD_VisReports" {
   component "ReportView\nScheduledReportView\nSavedViewView\nMetricView" as ReportView <<api>>
   component "ReportContract\nScheduledReportSerializer\nExportJobSerializer" as ReportContract <<serializer>>
   component "ReportService\nfiltrar Report por ReportScope\ngestionar ScheduledReport y SavedView\nencolar ExportJob" as ReportService <<service>>
   component "ReportRepository\nScheduledReportRepository\nSavedViewRepository\nMetricRepository\nExportJobRepository" as ReportRepo <<repository>>
   component "ReportORM\nScheduledReportORM\nSavedViewORM\nMetricORM\nExportJobORM" as ReportORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 ReportView --> ReportContract : valida
 ReportView --> ReportService : invoca
 ReportService --> ReportRepo : consulta / persiste
 ReportRepo --> ReportORM : mapea
 ReportORM --> AlmacenDatos : SQL

 note right of ReportService
   Report.filter(ReportScope.AGENTS|CAMPAIGNS|QUEUES).
   ScheduledReport: ejecucion periodica automatizada.
   SavedView: vistas filtradas persistidas por usuario.
   ExportJob{format:PDF|CSV, state:QUEUED→DONE}.
   Metric: metricas agregadas por periodo.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/report`
 :doc:`/arquitectura-tecnica/domain-model/metric`
 :doc:`/arquitectura-tecnica/domain-model/export-job`
 :doc:`/arquitectura-tecnica/domain-model/scheduled-report`
 :doc:`/arquitectura-tecnica/domain-model/saved-view`
