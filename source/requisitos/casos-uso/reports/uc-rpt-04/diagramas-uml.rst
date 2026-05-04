.. _uc-rpt-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_04 — export

 @startuml
 left to right direction
 actor "export_csv" as export_csv
 actor "ExportWorker" as Exportworker
 actor "MailboxService" as Mailboxservice

 rectangle "MOD_Reports" {
   usecase "UC_RPT_04\nExport" as UC04
   usecase "Encolar Job" as Q
   usecase "Audit eventos" as A
   usecase "Notify mailbox" as N
 }

 export_csv --> UC04
 UC04 ..> Q : <<include>>
 UC04 ..> A : <<include>>
 Exportworker ..> A : <<include>>
 Exportworker ..> N : <<include>>
 N --> Mailboxservice

 note bottom
   Async via worker. URL firmado
   TTL 24h. CNST-002 mailbox.
 end note

 @enduml

8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_04 — flujo

 @startuml
 start
 :POST /api/reports/export/;
 if (JWT?) then (no)
   :401; stop
 endif
 if (export_csv?) then (no)
   :403 + audit; stop
 endif
 :Validar payload + estimacion;
 if (Excede limites?) then (si)
   :400; stop
 endif
 if (User > 5 jobs?) then (si)
   :429; stop
 endif
 :Crear ExportJob;
 :Encolar en worker;
 :Audit REPORT_EXPORT_QUEUED;
 :202 con job_id;
 :Worker toma job;
 :Recheck permiso del User;
 if (Permiso revocado?) then (si)
   :failed PERMISSION_REVOKED;
   stop
 endif
 :Stream query Analytics;
 :Sanitizar + escribir archivo;
 if (> 200 MB?) then (si)
   :failed TOO_LARGE; stop
 endif
 :Subir a storage + URL firmado;
 :Audit REPORT_EXPORT_COMPLETED;
 :Notify mailbox del User;

 stop
 @enduml

8.3 Diagrama de estado
======================

.. uml::
 :caption: ExportJob

 @startuml
 [*] --> queued
 queued --> running : worker pickup
 queued --> cancelled : DELETE
 running --> done : ok
 running --> failed : error
 running --> cancelled : cancellation_requested
 done --> expired : 24h
 failed --> [*]
 cancelled --> [*]
 expired --> [*]
 @enduml

8.4 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_RPT_04 — sync + async

 @startuml
 actor "User" as User
 participant "Endpoint" as Endpoint
 participant "JobRepo" as Jobrepo
 queue "Worker" as Worker
 database "Analytics" as Analytics
 participant "Storage" as Storage
 participant "Mailbox" as Mailbox
 participant "AuditSvc" as Auditsvc

 User -> Endpoint: POST /export
 Endpoint -> Endpoint: JWT + RBAC + validar
 Endpoint -> Jobrepo: create(job)
 Jobrepo --> Endpoint: job_id
 Endpoint -> Auditsvc: emit QUEUED
 Endpoint -> Worker: enqueue(job_id)
 Endpoint --> User: 202 + job_id

 ... background ...

 Worker -> Jobrepo: load(job_id)
 Worker -> Worker: re-check permiso
 Worker -> Analytics: stream query
 Analytics --> Worker: rows
 Worker -> Storage: upload file
 Storage --> Worker: url
 Worker -> Jobrepo: update(done, url, ...)
 Worker -> Auditsvc: emit COMPLETED
 Worker -> Mailbox: notify(user, url)
 @enduml
