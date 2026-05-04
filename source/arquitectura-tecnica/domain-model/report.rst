.. meta::
 :artefacto: AT_DM_CLASS_REPORT
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_report:

======
Report
======

Reporte del sistema IACT. Los distintos tipos de reporte se modelan
como instancias de ``Report`` con un atributo ``scope`` enumerado,
no como subclases (D-10). Los siete ``ReportScope`` canonicos cubren
los 17 UCs del cluster RPT.

.. uml::
 :caption: Clase Report — reporte con scope canonico.

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

 Report -- ReportScope
 Report -- ReportState

 note right of Report
   D-10: scope es atributo, no subclase.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-reports`
 :doc:`/arquitectura-tecnica/domain-model/export-job`
 :doc:`/arquitectura-tecnica/domain-model/scheduled-report`
 :doc:`/arquitectura-tecnica/domain-model/saved-view`
