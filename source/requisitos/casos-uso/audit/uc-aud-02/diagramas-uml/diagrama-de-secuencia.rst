.. _uc-aud-02-parte-08-diagrama-secuencia:

8.4 Diagrama de secuencia
==========================

.. uml::
 :caption: UC_AUD_02 — busqueda FTS en audit log.

 @startuml

 actor "search_audit_log" as search_audit_log
 participant "Servicio de Aplicacion" as SvcAplicacion
 participant "FTS Index" as FtsIndex
 participant "PIIScanner" as PIIScanner
 participant "AuditService" as AuditService

 search_audit_log -> SvcAplicacion: POST /api/v1/audit/search/
 SvcAplicacion -> SvcAplicacion: verificar capability\n+ validar query
 SvcAplicacion -> SvcAplicacion: throttle check (rate limit)

 SvcAplicacion -> FtsIndex: search(query, range, filters)
 FtsIndex --> SvcAplicacion: hits + ranking

 SvcAplicacion -> PIIScanner: sanitize(hits)
 PIIScanner --> SvcAplicacion: clean hits

 SvcAplicacion -> AuditService: emit AUDIT_SEARCH_QUERIED\n  (query, hits_count)
 SvcAplicacion --> search_audit_log: 200 + results

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-actividad`.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`.
