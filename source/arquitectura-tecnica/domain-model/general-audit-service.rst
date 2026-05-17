.. meta::
 :artefacto: AT_DM_CLASS_GENERAL_AUDIT_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_general_audit_service:

====================
GeneralAuditService
====================

Servicio de aplicacion que provee consulta general del log
de auditoria con paginacion via cursor + sanitizacion PII.
Es la cara consultiva del BC Audit, complementaria a:

- ``AuditService`` — escritura de eventos (``emit``).
- ``AuditQueryService`` — queries especializadas para
  endpoints especificos.

Distinto de los anteriores: ``GeneralAuditService`` es el
endpoint generico ``GET /api/v1/audit/`` que un user con
codename ``view_audit`` invoca con filtros libres.

.. uml::
 :caption: GeneralAuditService — consulta general del audit
           log con paginacion cursor y sanitizacion PII.

 @startuml

 class GeneralAuditService {
   --
   + query(filters : AuditFilters, \
            cursor : Cursor, \
            actor_scope : SegmentScope) : AuditQueryResult
 }

 class AuditFilters {
   + event_type : String
   + actor_user_id : UUID
   + entity_id : UUID
   + period : DateRange
 }

 class AuditQueryResult {
   + events : List<AuditEvent>
   + next_cursor : Cursor
   + total_estimate : Integer
 }

 class AuditRepo
 class CursorEncoder
 class PIIScanner
 class AuditService

 GeneralAuditService --> AuditRepo : queries
 GeneralAuditService --> CursorEncoder : paginates
 GeneralAuditService --> PIIScanner : sanitizes
 GeneralAuditService --> AuditService : emits meta-audit
 GeneralAuditService ..> AuditFilters
 GeneralAuditService ..> AuditQueryResult

 @enduml

Operaciones principales
=======================

- ``query(filters, cursor, actor_scope)`` — pipeline:

  1. Decodifica el cursor para resumir desde la pagina
     correcta.
  2. Lee de ``AuditRepo`` con ``filters`` aplicados.
  3. Sanitiza PII via ``PIIScanner`` antes de exponer.
  4. Filtra por ``actor_scope`` (CNST-018).
  5. Genera el ``next_cursor``.
  6. Emite meta-audit (la consulta de audit es a su vez
     auditable).
  7. Empaqueta ``AuditQueryResult``.

Restricciones aplicables
========================

- **CNST-018** — el resultado se filtra por scope del user
  consultor.
- **CNST-025** — la consulta general se audita (meta-audit).
- **CNST-027** — sanitizacion PII obligatoria en exposicion
  externa.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/audit/uc-aud-01/index` —
  consulta general de audit log.

Relaciones
==========

- Lee ``AuditRepo``.
- Pagina via ``CursorEncoder``.
- Sanitiza con ``PIIScanner``.
- Emite meta-audit via ``AuditService``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo`
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service`
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder`
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`
