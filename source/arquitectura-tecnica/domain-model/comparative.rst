.. meta::
 :artefacto: AT_DM_CLASS_COMPARATIVE
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

.. _dm_class_comparative:

===========
Comparative
===========

Comparativa de KPIs entre periodo actual y periodo anterior dentro de un HistoricalReport.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase Comparative — stub pendiente de desarrollo.

 @startuml

 class Comparative {
  + period_prior : Period
  + kpis_summary : KPISet
  + diff_pct : Double
 }

 @enduml
