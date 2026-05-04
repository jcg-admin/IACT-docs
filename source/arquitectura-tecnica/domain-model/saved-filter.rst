.. meta::
 :artefacto: AT_DM_CLASS_SAVED_FILTER
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_saved_filter:

===========
SavedFilter
===========

Filtro guardado reutilizable no atado a un Report especifico. Distinto de SavedView.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase SavedFilter — stub pendiente de desarrollo.

 @startuml

 class SavedFilter {
  + id : UUID
  + name : String
  + filters : List<Filter>
  + period_relative : String
  + applies_to : String
  + is_default : Boolean
  + is_invalid : Boolean
 }

 @enduml
