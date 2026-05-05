.. meta::
 :artefacto: AT_DM_CLASS_SAVED_FILTER
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

.. _dm_class_saved_filter:

===========
SavedFilter
===========

Filtro guardado reutilizable. A diferencia de
``SavedView`` (que almacena la configuración completa del
reporte), ``SavedFilter`` captura solo el conjunto de
filtros + período relativo, aplicable a múltiples tipos de
reportes (``applies_to``).

Marca ``is_invalid`` cuando un filtro contiene referencias
a entidades que ya no existen (e.g. cola eliminada),
permitiendo al UI alertar al usuario antes de aplicar.

.. uml::
 :caption: Clase SavedFilter — filtro nominado reutilizable
           con período relativo.

 @startuml

 class SavedFilter {
   + filter_id : UUID
   + owner_user_id : UUID
   + name : String
   + filters : List<FilterClause>
   + period_relative : RelativePeriod
   + applies_to : Set<ReportType>
   + is_default : Boolean
   + is_invalid : Boolean
   + created_at : DateTime
   + last_used_at : DateTime
   --
   + applies_to_report(report_type : ReportType) : Boolean
   + resolve_period(now : DateTime) : Period
   + mark_invalid(reason : String) : void
   + use() : void
 }

 class FilterClause {
   + field : String
   + operator : FilterOperator
   + value : Object
 }

 enum FilterOperator {
   EQ
   NEQ
   IN
   NOT_IN
   GT
   GTE
   LT
   LTE
   CONTAINS
 }

 enum RelativePeriod {
   LAST_24H
   LAST_7D
   LAST_30D
   LAST_90D
   THIS_MONTH
   PREVIOUS_MONTH
   YEAR_TO_DATE
 }

 enum ReportType {
   DASHBOARD
   REALTIME
   HISTORICAL
   AGENT
   QUEUE
   CAMPAIGN
   TRANSFER
   IVR
   UNIQUE_CLIENTS
 }

 SavedFilter *-- "*" FilterClause : composes
 SavedFilter -- RelativePeriod
 FilterClause -- FilterOperator

 note right of SavedFilter
   period_relative se resuelve a Period
   absoluto al momento de uso
   (resolve_period(now)).
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-09/index`
  — configurar filtros (CRUD de ``SavedFilter``).

Relaciones
==========

- Compone (``*--``) ``FilterClause``: cláusulas no
  tienen sentido sin el filter padre.
- Asociado con ``User`` por ``owner_user_id``
  (referencia, no FK fuerte).
