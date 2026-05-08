.. meta::
 :artefacto: AT_DM_CLASS_COMPARATIVE
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

.. _dm_class_comparative:

===========
Comparative
===========

Comparativa de KPIs entre el período actual y un período
anterior. Permite presentar evolución temporal en reportes
históricos: variación absoluta, variación porcentual y
tendencia (mejora / deterioro / estable) por KPI.

Es DTO inmutable: una vez calculada, no se altera.

.. uml::
 :caption: Clase Comparative — variaciones de KPI entre
           período actual y anterior.

 @startuml

 class Comparative {
   + period_current : Period
   + period_prior : Period
   + kpis_summary : KPISet
   + diff_pct_by_kpi : Map<String, Double>
   + trend_by_kpi : Map<String, Trend>
   --
   + get_diff_pct(kpi_name : String) : Double
   + get_trend(kpi_name : String) : Trend
   + has_significant_change(kpi_name : String, threshold : Double) : Boolean
 }

 class Period {
   + start : DateTime
   + end : DateTime
   --
   + duration() : Duration
 }

 enum Trend {
   IMPROVING
   DETERIORATING
   STABLE
   INSUFFICIENT_DATA
 }

 class KPISet

 Comparative *-- "2" Period : composes
 Comparative "1" *-- "1" KPISet : composes
 Comparative "1" ..> "0..*" Trend : returns

 note right of Comparative
   trend_by_kpi mejora / deterioro
   por KPI segun su semantica
   (TMO menor = mejor; SL mayor = mejor).
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-03/index` —
  reportes históricos con comparativa.
- :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`
  — reporte agentes con período comparado.

Relaciones
==========

- Compone (``*--``) dos ``Period`` (current + prior).
- Compone un ``KPISet`` con los valores agregados.
- Devuelve ``Trend`` por KPI (lookup map).
