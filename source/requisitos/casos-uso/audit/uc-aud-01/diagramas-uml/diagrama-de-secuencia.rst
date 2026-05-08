.. _uc-aud-01-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_AUD_01 — consulta de audit log con paginacion cursor.

 @startuml

 actor "view_audit_log" as view_audit_log
 participant "Servicio de Aplicacion" as SvcAplicacion
 database   "AuditRepo" as AuditRepo
 participant "PIIScanner" as PIIScanner
 participant "CursorEncoder" as CursorEncoder
 participant "AuditService" as AuditService

 view_audit_log -> SvcAplicacion: GET /api/v1/audit/?filters&cursor
 SvcAplicacion -> SvcAplicacion: verificar capability\nview_audit_log

 SvcAplicacion -> CursorEncoder: decode(cursor)
 CursorEncoder --> SvcAplicacion: state

 SvcAplicacion -> AuditRepo: query(filters, state)
 AuditRepo --> SvcAplicacion: rows

 SvcAplicacion -> PIIScanner: sanitize(rows)
 PIIScanner --> SvcAplicacion: clean rows

 SvcAplicacion -> CursorEncoder: encode(next_state)
 CursorEncoder --> SvcAplicacion: next_cursor

 SvcAplicacion -> AuditService: emit GENERAL_AUDIT_QUERIED
 SvcAplicacion --> view_audit_log: 200 + rows + next_cursor

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`.
