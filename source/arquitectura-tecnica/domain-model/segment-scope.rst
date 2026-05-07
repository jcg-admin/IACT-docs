.. meta::
 :artefacto: AT_DM_CLASS_SEGMENT_SCOPE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_segment_scope:

============
SegmentScope
============

Value Object que representa el alcance de segmentos visibles
para un usuario en el contexto de reportes y suscripciones.
Es el resultado de resolver, via ``SegmentResolver``, las
capabilities efectivas del usuario contra el catalogo de
segmentos vigentes.

Distinto de ``SegmentResolver`` (servicio que lo computa),
``SegmentScope`` es un objeto de valor inmutable consumido
por queries de reporte para filtrar resultados al alcance
del usuario.

.. uml::
 :caption: SegmentScope — alcance de segmentos visibles
           del usuario.

 @startuml

 class SegmentScope {
   + segments : Set<Segment>
   + es_global : Boolean
   --
   + contains(segment_id : UUID) : Boolean
   + intersect(other : SegmentScope) : SegmentScope
   + as_filter() : QueryFilter
 }

 class Segment {
   + id : UUID
   + kind : SegmentKind
   + ref : String
 }

 enum SegmentKind {
   QUEUE
   SKILL
   DEPARTMENT
   ALL
 }

 SegmentScope "1" --> "*" Segment : contains
 Segment ..> SegmentKind

 @enduml

Atributos
=========

- ``segments : Set<Segment>`` — conjunto explicito de
  segmentos visibles. Vacio + ``es_global=true`` significa
  acceso a todo.
- ``es_global : Boolean`` — flag para usuarios con codename
  global (admin con ``view_all_segments``).

Operaciones principales
=======================

- ``contains(segment_id)`` — verifica si el segmento esta
  en el scope (constante O(1) con set).
- ``intersect(other)`` — interseccion con otro scope; util
  cuando un report tiene su propio filtro y se aplica
  encima del scope del user.
- ``as_filter()`` — convierte el scope a un ``QueryFilter``
  aplicable a queries SQL.

Restricciones aplicables
========================

- **CNST-018** — segmentos visibles son derivados del
  catalogo RBAC; no se exponen segmentos no autorizados.
- **BR-012** — usuarios con ``segment_id`` heredado pueden
  tener scope expandido por configuracion.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index` —
  computo de scope inicial en login.
- Consumido por todos los UCs de cluster ``reports`` para
  filtrar resultados.

Relaciones
==========

- Producido por ``SegmentResolver.resolve_for_user``.
- Consumido por todos los servicios ``*ReportService`` para
  filtrar queries antes de exponer resultados al user.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`
 - :doc:`/arquitectura-tecnica/domain-model/rbac-repo`
