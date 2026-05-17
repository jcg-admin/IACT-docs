.. _uc-aud-03-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_AUD_03 — exportacion asincrona del audit log.

 @startuml

 actor "export_audit_log" as export_audit_log
 participant "Servicio de Aplicacion" as SvcAplicacion
 participant "ExportWorker" as ExportWorker
 database   "AuditRepo" as AuditRepo
 participant "InternalMailbox" as InternalMailbox
 participant "AuditService" as AuditService

 export_audit_log -> SvcAplicacion: POST /api/v1/audit/export/ {filters}
 SvcAplicacion -> SvcAplicacion: verificar capability\n+ validar filtros

 alt sin capability
   SvcAplicacion --> export_audit_log: 403 Forbidden
 else con capability
   SvcAplicacion -> ExportWorker: encolar job
   SvcAplicacion -> AuditService: emit AUDIT_EXPORT_QUEUED
   SvcAplicacion --> export_audit_log: 202 Accepted + job_id

   ExportWorker -> AuditRepo: query por filtros
   AuditRepo --> ExportWorker: rows
   ExportWorker -> ExportWorker: formatear CSV/JSON\n+ sanitize PII
   ExportWorker -> InternalMailbox: entregar archivo
   ExportWorker -> AuditService: emit AUDIT_EXPORT_DELIVERED
   InternalMailbox --> export_audit_log: archivo disponible
 end

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/export-job`.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`.
