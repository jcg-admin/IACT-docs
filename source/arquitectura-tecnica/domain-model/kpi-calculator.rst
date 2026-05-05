.. meta::
 :artefacto: AT_DM_CLASS_KPI_CALCULATOR
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

.. _dm_class_kpi_calculator:

=============
KPICalculator
=============

Componente puro (stateless) que **calcula KPIs derivados**
a partir de estadísticas crudas. Centraliza las fórmulas
canónicas para evitar divergencia entre reportes (ej.
"AHT" calculado de la misma forma en agente y queue).

Cada método toma una estructura cruda (``AgentStats``,
``QueueStats``, ``CampaignStats``) y devuelve un ``KPISet``
con los valores derivados nombrados.

.. uml::
 :caption: Clase KPICalculator — fórmulas canónicas para
           KPIs derivados (stateless).

 @startuml

 class KPICalculator {
   --
   + derive_agent_kpis(stats : AgentStats) : KPISet
   + derive_queue_kpis(stats : QueueStats) : KPISet
   + derive_campaign_kpis(stats : CampaignStats) : KPISet
   + derive_global_kpis(stats : List<AgentStats>) : KPISet
   - safe_divide(numerator : Double, denominator : Double) : Double
   - percentage(part : Double, total : Double) : Double
 }

 class KPISet
 class AgentStats
 class QueueStats
 class CampaignStats

 KPICalculator ..> AgentStats : reads
 KPICalculator ..> QueueStats : reads
 KPICalculator ..> CampaignStats : reads
 KPICalculator ..> KPISet : returns

 note right of KPICalculator
   Stateless. safe_divide previene
   division por cero (devuelve 0
   o null segun politica del KPI).
 end note

 @enduml

KPIs canónicos calculados
=========================

**Agente:**

- ``occupancy_pct`` = ``handled_time / staffed_time``
- ``aht`` = ``total_handle_time / total_calls`` (Average
  Handle Time)
- ``acw`` = ``total_acw_time / total_calls`` (After Call
  Work avg)
- ``adherence_pct`` = ``actual_login_time /
  scheduled_login_time``

**Queue:**

- ``service_level_pct`` = ``calls_in_target /
  calls_offered`` (típicamente con target 20s)
- ``abandonment_rate`` = ``calls_abandoned /
  calls_offered``
- ``asa`` = ``total_wait_time / calls_answered`` (Average
  Speed of Answer)

**Campaign:**

- ``contact_rate`` = ``contacts_made / dials_attempted``
- ``conversion_rate`` = ``conversions / contacts_made``
- ``cost_per_acquisition`` = ``total_cost / conversions``

Restricciones aplicables
========================

- **Determinismo**: dado el mismo stats input, el output
  es idéntico.
- **No estado**: usable concurrentemente sin sync.
- ``safe_divide`` y ``percentage`` evitan ``NaN`` /
  ``Infinity`` ante denominadores cero.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`
  (agentes).
- :doc:`/requisitos/casos-uso/reports/uc-rpt-13/index`
  (colas).
- :doc:`/requisitos/casos-uso/reports/uc-rpt-14/index`
  (campañas).

Relaciones
==========

- Lee ``AgentStats``, ``QueueStats``, ``CampaignStats``
  (DTOs de repos correspondientes).
- Devuelve ``KPISet`` consumido por ``Bucket`` y
  ``HistoricalReport``.
