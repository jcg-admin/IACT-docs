.. meta::
 :artefacto: AT_DM_CLASS_HISTORICAL_REPORT
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

.. _dm_class_historical_report:

================
HistoricalReport
================

Reporte agregado de KPIs sobre un período, agrupado por una
dimensión (``group_by``). Es la entidad central del bounded
context Reports: cada UC de tipo "ver reporte" produce un
``HistoricalReport`` consumible por el frontend.

Mantiene un set ordenado de ``Bucket`` (uno por valor de la
dimensión de agrupación) y opcionalmente una ``Comparative``
si el período anterior está disponible.

.. uml::
 :caption: Clase HistoricalReport — agregación de Buckets
           con comparativa opcional sobre un período.

 @startuml

 class HistoricalReport {
   + report_id : UUID
   + period : Period
   + group_by : Dimension
   + buckets : List<Bucket>
   + comparative : Comparative
   + filters_applied : ReportFilters
   + generated_at : DateTime
   --
   + total_buckets() : Integer
   + bucket_for_key(key : String) : Bucket
   + has_comparative() : Boolean
   + summary_kpis() : KPISet
 }

 enum Dimension {
   HOUR_OF_DAY
   DAY
   WEEK
   MONTH
   AGENT
   QUEUE
   CAMPAIGN
   IVR_NODE
 }

 class Period
 class Bucket
 class Comparative
 class ReportFilters

 HistoricalReport *-- Period : composes
 HistoricalReport *-- "*" Bucket : composes
 HistoricalReport o-- Comparative : optionally has
 HistoricalReport *-- ReportFilters : composes
 HistoricalReport -- Dimension

 note right of HistoricalReport
   Agregacion por Dimension determina
   el sentido de bucket_key (hora,
   nombre de agente, codigo de cola, etc.).
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-03/index` —
  UC principal de reportes históricos.
- :doc:`/requisitos/casos-uso/reports/uc-rpt-04/index` —
  exportación de ``HistoricalReport``.
- Indirectamente todos los UCs ``uc-rpt-*`` que producen
  reportes con grouping.

Relaciones
==========

- Compone múltiples ``Bucket`` (1 por valor de la
  dimensión).
- Compone un ``Period`` y los ``ReportFilters``
  aplicados.
- Agregación opcional con ``Comparative``.
