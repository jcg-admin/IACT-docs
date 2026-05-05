.. meta::
 :artefacto: AT_DM_CLASS_BUCKET
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

.. _dm_class_bucket:

======
Bucket
======

Unidad atómica de agrupación dentro de un
``HistoricalReport``: cada bucket representa los KPIs
calculados para una clave dimensional (e.g. una hora del
día, una cola, un agente). El reporte completo es un set
ordenado de buckets.

Es un DTO inmutable: una vez calculado, no se modifica.
Los KPIs internos se acceden por nombre vía el ``KPISet``
embebido.

.. uml::
 :caption: Clase Bucket — agregación inmutable de KPIs por
           clave dimensional dentro de un HistoricalReport.

 @startuml

 class Bucket {
   + bucket_key : String
   + kpis : KPISet
   + sample_count : Integer
   + period_start : DateTime
   + period_end : DateTime
   --
   + get_kpi(name : String) : Double
   + has_kpi(name : String) : Boolean
   + is_empty() : Boolean
 }

 class KPISet {
   + values : Map<String, Double>
   --
   + get(name : String) : Double
   + names() : Set<String>
   + size() : Integer
 }

 Bucket *-- KPISet : composes

 note right of Bucket
   Inmutable. sample_count > 0 garantiza
   que los KPIs son significativos
   (no extrapolacion sobre 0 muestras).
 end note

 @enduml

Trazabilidad a UCs
==================

Subset de UCs que producen ``Bucket``:

- :doc:`/requisitos/casos-uso/reports/uc-rpt-01/index`
  (dashboard real-time)
- :doc:`/requisitos/casos-uso/reports/uc-rpt-03/index`
  (reportes históricos)
- :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`
  (reporte agentes)

Relaciones
==========

- Compone (``*--``) un ``KPISet``: el set no tiene
  sentido fuera del bucket que lo contiene.
- Pertenece (``*..1``) a un ``HistoricalReport``.
