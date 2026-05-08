.. meta::
 :artefacto: AT_DESIGN_SEQ_AUDIT
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: audit
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_audit:

============================================================
Design View — MOD_Audit: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Audit: query de eventos de
auditoria con filtros + paginacion cursor (CursorEncoder).
Verificacion previa del filtro (FilterValidator) y validacion
sin PII en respuesta (CNST-026).

.. uml::
 :caption: MOD_Audit — query con filtros y cursor pagination.

 @startuml

 actor "view_audit_log" as view_audit_log
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "AuditQueryService" as AuditQueryService <<sistema>>
 actor "FilterValidator" as FilterValidator <<sistema>>
 actor "CursorEncoder" as CursorEncoder <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>

 view_audit_log -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> view_audit_log : OK
 deactivate AuthorizationGuard

 view_audit_log -> AuditQueryService : query(filters, cursor?)
 activate AuditQueryService

 AuditQueryService -> FilterValidator : validate(filters)
 activate FilterValidator
 FilterValidator --> AuditQueryService : OK
 deactivate FilterValidator

 alt cursor presente
   AuditQueryService -> CursorEncoder : decode(cursor)
   activate CursorEncoder
   CursorEncoder --> AuditQueryService : pagination_state
   deactivate CursorEncoder
 end

 AuditQueryService -> AuditRepo : query(state)
 activate AuditRepo
 AuditRepo --> AuditQueryService : List<AuditEvent>
 deactivate AuditRepo

 AuditQueryService -> CursorEncoder : encode(next_state)
 activate CursorEncoder
 CursorEncoder --> AuditQueryService : next_cursor
 deactivate CursorEncoder

 AuditQueryService --> view_audit_log : {events, next_cursor}
 deactivate AuditQueryService

 note right of AuditQueryService
   CNST-026: respuesta sin PII
   (validado por AuditValidator
   en escritura, garantia leida).
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/class-audit`
 - :doc:`/arquitectura-tecnica/use-case-view/audit/index`
 - :doc:`/arquitectura-tecnica/domain-model/audit-event`
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo`
 - :doc:`/arquitectura-tecnica/domain-model/filter-validator`
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
