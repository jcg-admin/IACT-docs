.. meta::
 :artefacto: AT_DM_CLASS_HISTORICAL_REPORT
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

.. _dm_class_historical_report:

================
HistoricalReport
================

Reporte historico con agrupacion por periodo y comparativa. Contiene Buckets de KPIs.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase HistoricalReport — stub pendiente de desarrollo.

 @startuml

 class HistoricalReport {
  + period : Period
  + group_by : String
  + buckets : List<Bucket>
  + comparative : Comparative
 }

 @enduml
