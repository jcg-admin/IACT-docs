.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_QUERY_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_audit_query_service:

=================
AuditQueryService
=================

Servicio orientado a la **lectura** del repositorio de
auditoría. Expone consultas paginadas (cursor-based),
agregaciones por dimensión y exportación asíncrona delegada al
``ExportWorker``.

Toda consulta requiere autorización RBAC (``view_audit_log``
o sub-permisos como ``search_audit_log`` y
``export_audit_log``) y aplica filtrado por scope para que un
usuario nunca vea más allá de su perímetro de visibilidad
declarado.

.. uml::
 :caption: Clase AuditQueryService — fachada de lectura del
           almacén de auditoría con paginación cursor-based.

 @startuml

 class AuditQueryService {
   - repo : AuditRepo
   - cursor_encoder : CursorEncoder
   - export_worker : ExportWorker
   - sanitizer : Sanitizer
   --
   + list(filters : AuditFilters, cursor : String, \
          page_size : Integer) : ListPage
   + get(event_id : UUID) : AuditEventView
   + search(query : SearchQuery) : SearchResult
   + aggregate(filters : AuditFilters, \
                group_by : List<String>) : AggregateResult
   + export(filters : AuditFilters, format : ExportFormat) : ExportJob
   - apply_scope(filters : AuditFilters, \
                  invoker : User) : AuditFilters
   - sanitize_for_view(event : AuditEvent) : AuditEventView
 }

 class ListPage {
   + items : List<AuditEventView>
   + next_cursor : String
   + total_estimate : Integer
 }

 class AuditEventView {
   + event_id : UUID
   + event_type : EventType
   + actor_username : String
   + occurred_at : DateTime
   + summary : String
 }

 enum ExportFormat {
   CSV
   JSON
   PDF
 }

 class ExportJob

 AuditQueryService o-- AuditRepo : reads
 AuditQueryService *-- CursorEncoder : composes
 AuditQueryService o-- ExportWorker : enqueues
 AuditQueryService *-- Sanitizer : composes
 AuditQueryService ..> ListPage : returns
 AuditQueryService ..> ExportJob : returns
 AuditQueryService ..> ExportFormat : uses

 note right of AuditQueryService
   Filtros RBAC aplicados antes de consultar
   el repositorio (apply_scope).
 end note

 @enduml

Restricciones aplicables
========================

- **CNST-008** — segmentos: filtros adicionales por
  segmento del invocador.
- **CNST-026** — sanitización de PII en
  ``sanitize_for_view`` antes de devolver al usuario.
- **P-15** — RBAC granular: ``view_audit_log`` /
  ``search_audit_log`` / ``export_audit_log`` distintos.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/audit/uc-aud-01/index` —
  ``list``
- :doc:`/requisitos/casos-uso/audit/uc-aud-02/index` —
  ``search``
- :doc:`/requisitos/casos-uso/audit/uc-aud-03/index` —
  ``export``
- :doc:`/requisitos/casos-uso/audit/uc-aud-04/index` —
  ``aggregate`` (compliance report)
- :doc:`/requisitos/casos-uso/permissions/uc-perm-10/index`
  — vista RBAC del audit

Relaciones
==========

- Agregación con ``AuditRepo`` (lectura, no posee).
- Composición con ``CursorEncoder`` (encoder es interno).
- Agregación con ``ExportWorker`` (worker tiene ciclo de vida
  propio).
- Devuelve ``AuditEventView`` (proyección saneada de
  ``AuditEvent``).
