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
