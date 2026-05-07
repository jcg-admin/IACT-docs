.. _uc-log-04-parte-08-diagrama-secuencia-exportacion-logs:

8.4 Diagrama de secuencia — Exportacion de logs
=================================================

.. uml::
 :caption: UC_LOG_04 — flujo asincrono.

 @startuml

 actor "export_logs" as export_logs
 participant "Servicio de Aplicacion" as SvcAplicacion
 participant "ExportWorker" as ExportWorker
 database   "LogStore" as LogStore
 participant "InternalMailbox" as InternalMailbox
 participant "AuditService" as AuditService

 export_logs -> SvcAplicacion : POST /api/v1/logs/export/
 SvcAplicacion -> SvcAplicacion : verificar capability + validar
 SvcAplicacion -> ExportWorker : encolar job
 SvcAplicacion -> AuditService : emit LOG_EXPORT_QUEUED
 SvcAplicacion --> export_logs : 202 Accepted con job_id

 ExportWorker -> LogStore : query rango
 LogStore --> ExportWorker : entries
 ExportWorker -> ExportWorker : sanitize + format
 ExportWorker -> InternalMailbox : adjuntar archivo
 ExportWorker -> AuditService : emit LOG_EXPORT_DELIVERED
 InternalMailbox --> export_logs : archivo disponible

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
