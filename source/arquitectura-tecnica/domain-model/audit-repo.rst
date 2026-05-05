.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_REPO
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

.. _dm_class_audit_repo:

=========
AuditRepo
=========

Repositorio append-only de ``AuditEvent``. Es el único punto
del sistema autorizado para escribir en el almacén de
auditoría. Por **CNST-025** las únicas operaciones permitidas
son ``append`` y consultas (``find``, ``get_by_id``,
``query``, ``aggregate``); las operaciones de modificación
(``update``, ``delete``) están explícitamente prohibidas y no
existen en la interfaz.

Provee primitivas de paginación cursor-based para consultas
de gran volumen y agregaciones para reportes de compliance.

.. uml::
 :caption: Clase AuditRepo — repositorio append-only para
           AuditEvent (CNST-025).

 @startuml

 class AuditRepo {
   - storage_backend : StorageBackend
   - retention_policy : RetentionPolicy
   --
   + append(event : AuditEvent) : UUID
   + append_batch(events : List<AuditEvent>) : List<UUID>
   + find(filters : AuditFilters, cursor : Cursor, limit : Integer) : QueryResult
   + get_by_id(event_id : UUID) : AuditEvent
   + count(filters : AuditFilters) : Integer
   + aggregate(filters : AuditFilters, group_by : List<String>) : AggregateResult
   + exists(event_id : UUID) : Boolean
 }

 class AuditFilters {
   + actor_user_id : UUID
   + event_type : EventType
   + target_entity_type : String
   + target_entity_id : String
   + occurred_at_from : DateTime
   + occurred_at_to : DateTime
 }

 class QueryResult {
   + events : List<AuditEvent>
   + next_cursor : Cursor
   + has_more : Boolean
 }

 class AggregateResult {
   + buckets : List<AggregateBucket>
   + total : Integer
 }

 class AuditEvent

 AuditRepo ..> AuditEvent : persists
 AuditRepo ..> AuditFilters : queries with
 AuditRepo ..> QueryResult : returns
 AuditRepo ..> AggregateResult : returns

 note right of AuditRepo
   CNST-025: append-only.
   Sin update, sin delete en la interfaz.
 end note

 @enduml

Operaciones explícitamente NO presentes
=======================================

Por **CNST-025** las siguientes operaciones están prohibidas y
no existen en la interfaz pública:

- ``update(event_id, changes)``
- ``delete(event_id)``
- ``purge(filters)``

Si una entidad consumidora necesita "actualizar" un evento, la
única vía válida es **emitir un nuevo evento** con tipo
``CORRECTION`` o equivalente referenciando al evento original
mediante ``details.references_event_id``.

Restricciones aplicables
========================

- **CNST-025** — append-only.
- **CNST-024** — retención según política
  (``RetentionPolicy``); archivado en frío sin perder
  inmutabilidad.
- **P-39** — auditoría reforzada: ``append_batch`` mantiene
  atomicidad por batch.

Trazabilidad a UCs
==================

Lectura:

- :doc:`/requisitos/casos-uso/audit/uc-aud-01/index` (consultar)
- :doc:`/requisitos/casos-uso/audit/uc-aud-02/index` (buscar)
- :doc:`/requisitos/casos-uso/permissions/uc-perm-10/index`
  (auditoría de permisos)

Escritura: indirecta vía ``AuditService.emit()``.

Relaciones
==========

- Usado por ``AuditService`` (escritura) y
  ``AuditQueryService`` (lectura).
- Persiste instancias de ``AuditEvent``.
- Asociado con ``RetentionPolicy`` para gestión de archivado.
