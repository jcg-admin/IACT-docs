.. _uc-perm-10-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_10 — consultar audit

 @startuml
 left to right direction

 actor "view_audit_log" as view_audit_log
 actor "ExportWorker" as Exportworker

 rectangle "MOD_Permissions / Audit" {
   usecase "UC_PERM_10\nList" as L
   usecase "Detalle" as D
   usecase "Aggregate" as A
   usecase "Export" as E
   usecase "UC_PERM_09\nmeta-audit" as M
 }

 view_audit_log --> L
 view_audit_log --> D
 view_audit_log --> A
 view_audit_log --> E
 L ..> M : <<include>>
 D ..> M : <<include>>
 A ..> M : <<include>>
 E ..> M : <<include>>
 E --> Exportworker
 Exportworker ..> M : <<include>>

 note bottom
   P-44: cada consulta del log
   se audita (audit del audit).
 end note

 @enduml

8.2 Diagrama de actividad (list)
================================

.. uml::
 :caption: UC_PERM_10 — list

 @startuml

 start
 :GET con filtros + cursor;
 if (JWT?) then (no)
   :401; stop
 endif
 if (view_audit_log?) then (no)
   :403 + UNAUTHORIZED audit;
   stop
 endif
 if (Filtros validos?) then (no)
   :400; stop
 endif
 :Query AuditRepo (read replica);
 :Sanitizar (truncar payload);
 :Construir cursor;
 :Estimar total;
 :Emit AUDIT_LOG_QUERIED (UC_PERM_09);
 if (Meta-audit ok?) then (no)
   :503; stop
 endif
 :200 OK;
 stop

 @enduml

8.3 Diagrama de clases
======================

.. uml::
 :caption: Estructura

 @startuml

 class AuditQueryService {
   list(filters, cursor, page_size)
   get(id)
   aggregate(filters, group_by)
   export(filters, format)
 }

 class AuditRepo {
   query(filters, cursor, limit)
   get_by_id(id)
   aggregate(filters, group_by)
 }

 class CursorEncoder {
   encode(last)
   decode(cursor)
 }

 class Sanitizer {
   truncate(payload)
 }

 class ExportWorker {
   enqueue(job)
   process(job)
 }

 AuditQueryService --> AuditRepo
 AuditQueryService --> CursorEncoder
 AuditQueryService --> Sanitizer
 AuditQueryService --> ExportWorker

 @enduml

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
