8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_audit_log" as view_audit_log
 participant "Endpoint" as Endpoint
 database "AuditRepo" as Auditrepo
 participant "AuditSvc" as Auditsvc
 view_audit_log -> Endpoint: GET /audit/
 Endpoint -> Endpoint: JWT + RBAC
 Endpoint -> Auditrepo: query
 Auditrepo --> Endpoint: rows
 Endpoint -> Auditsvc: emit GENERAL_AUDIT_QUERIED
 Endpoint --> view_audit_log: 200
 @enduml
