.. meta::
 :artefacto: AT_DM_CLASS_SEGMENT_RESOLVER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_segment_resolver:

===============
SegmentResolver
===============

Resuelve los segmentos de visibilidad aplicables a un
usuario al consultar reportes. Implementa **CNST-008**:
cada usuario tiene un perímetro de visibilidad
(segmentos: colas, campañas, agentes a los que tiene
acceso); todo reporte filtra por ese perímetro antes de
agregar.

El servicio combina assignments del usuario y reglas de
configuración del segmento (e.g. supervisor de equipo X
ve agentes de X).

.. uml::
 :caption: Clase SegmentResolver — resolución del scope
           de visibilidad por usuario (CNST-008).

 @startuml

 class SegmentResolver {
   - rbac_repo : RBACRepo
   - segment_config_repo : SegmentConfigRepo
   - cache : SegmentCache
   --
   + resolve(user_id : UUID) : Segment
   + resolve_for_report(user_id : UUID, report_type : ReportType) : Segment
   + has_access_to(user_id : UUID, entity_id : UUID, entity_type : EntityType) : Boolean
   - intersect(segments : List<Segment>) : Segment
 }

 class Segment {
   + queues : Set<UUID>
   + campaigns : Set<UUID>
   + agents : Set<UUID>
   + ivrs : Set<UUID>
   + is_global : Boolean
   --
   + contains_entity(entity_id : UUID, entity_type : EntityType) : Boolean
   + is_empty() : Boolean
 }

 enum EntityType {
   QUEUE
   CAMPAIGN
   AGENT
   IVR
 }

 class RBACRepo
 class SegmentConfigRepo
 class SegmentCache

 SegmentResolver o-- RBACRepo : reads
 SegmentResolver o-- SegmentConfigRepo : reads
 SegmentResolver *-- SegmentCache : composes
 SegmentResolver ..> Segment : returns
 Segment -- EntityType

 note right of SegmentResolver
   is_global = true para usuarios con
   permiso amplio (e.g. system_admin):
   bypass del filtro segmento.
 end note

 @enduml

Operaciones principales
=======================

- ``resolve(user_id)`` — devuelve ``Segment`` general del
  usuario (todos los entity types).
- ``resolve_for_report(user_id, report_type)`` — variante
  optimizada que solo retorna entity types relevantes para
  el tipo de reporte solicitado.
- ``has_access_to(user_id, entity_id, entity_type)`` —
  short circuit: ``true`` si el entity está en el segmento
  del usuario.

Restricciones aplicables
========================

- **CNST-008** — segmentación obligatoria.
- Cache TTL corto: cambios en assignment del usuario
  invalidan el cache (vía evento del bounded context
  RBAC).

Trazabilidad a UCs
==================

Consumido por todos los UCs ``uc-rpt-*`` antes de
consultar el repo de datos:

- :doc:`/requisitos/casos-uso/reports/uc-rpt-01/index`
- :doc:`/requisitos/casos-uso/reports/uc-rpt-03/index`
- :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`
- :doc:`/requisitos/casos-uso/reports/uc-rpt-13/index`

Relaciones
==========

- Agregación con ``RBACRepo`` y ``SegmentConfigRepo``
  (servicios externos).
- Composición con ``SegmentCache`` (componente interno).
- Devuelve ``Segment``.
