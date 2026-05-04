.. _uc-aud-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_audit_log" as view_audit_log
 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nConsultar Auditoria" as UC01
   usecase "UC_PERM_09\nMeta-audit" as M
 }
 view_audit_log --> UC01
 UC01 ..> M : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /audit/;
 :JWT + RBAC;
 :Validar;
 :Query AuditRepo + cursor;
 :Sanitize;
 :Build cursor;
 :Meta-audit GENERAL_AUDIT_QUERIED;
 if (Meta-audit ok?) then (no)
   :503; stop
 endif
 :200;
 stop
 @enduml

8.3 Clases
==========

.. uml::

 @startuml
 class GeneralAuditService
 class AuditRepo
 class CursorEncoder
 class AuditService
 GeneralAuditService --> AuditRepo
 GeneralAuditService --> CursorEncoder
 GeneralAuditService --> AuditService
 @enduml

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
