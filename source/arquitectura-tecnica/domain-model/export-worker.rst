.. meta::
 :artefacto: AT_DM_CLASS_EXPORT_WORKER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_export_worker:

============
ExportWorker
============

Worker asíncrono que ejecuta exportaciones de gran volumen
de ``AuditEvent`` a archivos descargables (CSV, JSON, PDF).
Se invoca por ``AuditQueryService.export()`` y opera
desacoplado del request HTTP del usuario, evitando
timeouts en exports masivos.

Implementa una cola de trabajos (``ExportJob``) con
estados explícitos. Aplica throttling para evitar saturar
el almacén de objetos y emite ``AuditEvent`` con tipo
``EXPORT_REQUESTED`` y ``EXPORT_COMPLETED`` para
trazabilidad.

.. uml::
 :caption: Clase ExportWorker — procesador asíncrono de
           jobs de exportación con throttling y notificación.

 @startuml

 class ExportWorker {
   - queue : JobQueue
   - storage : ObjectStorage
   - throttle_policy : ThrottlePolicy
   - notification_service : NotificationService
   --
   + enqueue(filters : AuditFilters, format : ExportFormat, \
             requester : User) : ExportJob
   + process_next() : ProcessResult
   + get_status(job_id : UUID) : JobStatus
   + cancel(job_id : UUID) : Boolean
   - render(events : List<AuditEvent>, format : ExportFormat) : Bytes
   - upload(content : Bytes, job_id : UUID) : URL
   - notify_completion(job : ExportJob) : void
 }

 class ExportJob {
   + job_id : UUID
   + requester_user_id : UUID
   + filters : AuditFilters
   + format : ExportFormat
   + status : JobStatus
   + enqueued_at : DateTime
   + started_at : DateTime
   + completed_at : DateTime
   + result_url : URL
   + error : String
 }

 enum JobStatus {
   QUEUED
   RUNNING
   COMPLETED
   FAILED
   CANCELLED
 }

 enum ExportFormat {
   CSV
   JSON
   PDF
 }

 class ProcessResult {
   + job_id : UUID
   + outcome : Outcome
   + duration_ms : Integer
 }

 enum Outcome {
   SUCCESS
   FAILURE
   THROTTLED
   CANCELLED
 }

 ExportWorker "1" ..> "0..*" ExportJob : creates/processes
 ExportWorker "1" ..> "0..*" ProcessResult : returns
 ExportJob "*" -- "1" JobStatus
 ExportJob "*" -- "1" ExportFormat
 ProcessResult "*" -- "1" Outcome

 note right of ExportWorker
   Asincrono. No bloquea HTTP request.
   Notifica via NotificationService al
   completar (CNST-002 buzon interno).
 end note

 @enduml

Estados del job (``JobStatus``)
===============================

- ``QUEUED`` — encolado, esperando turno.
- ``RUNNING`` — siendo procesado por un worker.
- ``COMPLETED`` — terminado, ``result_url`` disponible.
- ``FAILED`` — error durante procesamiento;
  ``error`` documenta motivo.
- ``CANCELLED`` — cancelado por el usuario o por timeout.

Restricciones aplicables
========================

- **CNST-019** — exportaciones asíncronas obligatorias
  (no bloquean request HTTP).
- **CNST-020** — throttling de exportaciones por
  recursos.
- **CNST-002** — notificación de completion via buzón
  interno, NUNCA por email externo.
- **CNST-026** — el ``render`` aplica sanitización
  adicional sobre los valores antes de escribirlos al
  archivo.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/audit/uc-aud-03/index` —
  exportar auditoría.
- :doc:`/requisitos/casos-uso/audit/uc-aud-04/index` —
  generar reporte compliance (ExportFormat = PDF).
- :doc:`/requisitos/casos-uso/permissions/uc-perm-10/index`
  — exportar log de permisos.

Relaciones
==========

- Agregado por ``AuditQueryService`` (worker tiene ciclo
  de vida propio).
- Agregación con ``JobQueue``, ``ObjectStorage``,
  ``ThrottlePolicy``, ``NotificationService`` (todos
  servicios externos del bounded context).
- Crea y procesa instancias de ``ExportJob``.
