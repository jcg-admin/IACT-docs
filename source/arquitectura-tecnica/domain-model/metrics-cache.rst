.. meta::
 :artefacto: AT_DM_CLASS_METRICS_CACHE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: CrossCutting
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _dm_class_metrics_cache:

============
MetricsCache
============

Cache de calculos KPI/metricas agregadas (Calls/TMO/SL/Adherence/etc.)
para evitar recomputar agregaciones costosas en cada request a un
reporte. TTL configurable por dataset; invalidacion explicita cuando
nuevos datos del Pipeline llegan o cuando cambia configuracion de
KPIs.

Consumido por ``KpiCalculator``, ``BaseReportService`` y los report
services especializados (``AgentReportService``, ``QueueReportService``,
``CampaignReportService``, etc.) para acelerar la generacion de
dashboards y vistas comparativas.

.. uml::
 :caption: Clase MetricsCache — cache de KPIs con TTL.

 @startuml

 class MetricsCache {
   - storage_backend : CacheBackend
   - default_ttl : Duration
   --
   + get(key : MetricKey) : MetricValue
   + set(key : MetricKey, value : MetricValue, ttl : Duration) : void
   + invalidate(key : MetricKey) : void
   + invalidate_by_dataset(dataset : String) : Integer
   + invalidate_by_period(period : Period) : Integer
   + warm(keys : List<MetricKey>) : void
   + hit_ratio() : Float
 }

 class MetricKey {
   + dataset : String
   + period : Period
   + segment_codes : List<String>
   + metric_name : String
   + group_by : String
 }

 MetricsCache --> MetricKey : usa

 note bottom of MetricsCache
   TTL default 5 min para metricas
   en vivo, 1h para historicas.
   Invalidacion explicita cuando
   Pipeline carga nuevos datos.
   CNST-007 read-only Analytics.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que consumen MetricsCache (lectura para reportes):

- :doc:`/requisitos/casos-uso/reports/uc-rpt-01/index` —
  dashboard IVR con auto-refresh.
- :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index` —
  reporte de agentes (TMO, AHT, Ocupacion, Adherence).
- :doc:`/requisitos/casos-uso/reports/uc-rpt-13/index` —
  reporte de colas (ASA, SL, Abandon rate).
- :doc:`/requisitos/casos-uso/operator/uc-opr-08/index` —
  dashboard propio del operador.

UCs que disparan invalidacion:

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
  retry de Pipeline invalida cache de metricas afectadas.

Relaciones
==========

- :doc:`kpi-calculator` — productor/consumidor del cache.
- :doc:`base-report-service` — usa cache via KpiCalculator.
- :doc:`metric` — entity individual cuyo agregado se cachea.
- :doc:`pipeline-execution` — disparador de invalidacion.
