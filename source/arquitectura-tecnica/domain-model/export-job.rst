.. meta::
 :artefacto: AT_DM_CLASS_EXPORT_JOB
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

.. _dm_class_export_job:

=========
ExportJob
=========

Trabajo de exportacion asincrona de un reporte. La exportacion se
encola (CNST-019 v3.0.0: cola abstracta) y procesa fuera de la
solicitud HTTP. Los limites de throttling (CNST-020) y formato
estan delegados al ADR de implementacion.

.. uml::
 :caption: Clase ExportJob — exportacion asincrona de reporte.

 @startuml

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

 enum ExportFormat {
   CSV
   EXCEL
   PDF
 }

 enum JobState {
   QUEUED
   PROCESSING
   DONE
   FAILED
 }

 ExportJob -- ExportFormat
 ExportJob -- JobState

 note right of ExportJob
   CNST-019 v3.0.0: cola asincrona abstracta.
   CNST-020 v3.0.0: throttling abstracto.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-reports`
 :doc:`/arquitectura-tecnica/domain-model/report`
