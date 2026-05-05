8.4 Diagrama de secuencia (export)
==================================

.. uml::
 :caption: UC_PERM_10 — export async

 @startuml

 actor "view_audit_log" as view_audit_log
 participant "ExportEndpoint" as Exportendpoint
 participant "QueryService" as Queryservice
 participant "ExportWorker" as Exportworker
 participant "MailboxService" as Mailboxservice
 database "AuditRepo" as Auditrepo
 participant "Storage" as Storage

 view_audit_log -> Exportendpoint: POST /export con filtros
 Exportendpoint -> Exportendpoint: JWT + RBAC + validar
 Exportendpoint -> Queryservice: enqueue(filters, format)
 Queryservice -> Exportworker: schedule(job)
 Exportworker --> Queryservice: job_id
 Queryservice -> Queryservice: emit AUDIT_LOG_EXPORT_QUEUED
 Queryservice --> Exportendpoint: 202 + job_id
 Exportendpoint --> view_audit_log: 202

 ... background ...
 Exportworker -> Auditrepo: query stream
 Auditrepo --> Exportworker: rows
 Exportworker -> Storage: write file
 Exportworker -> Exportworker: emit AUDIT_LOG_EXPORT_COMPLETED
 Exportworker -> Mailboxservice: notify(actor, file_url)

 ... auditor checks ...
 view_audit_log -> Exportendpoint: GET job_id
 Exportendpoint -> view_audit_log: status=done + file_url

 @enduml
