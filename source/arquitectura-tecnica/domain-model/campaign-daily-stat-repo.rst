.. meta::
 :artefacto: AT_DM_CLASS_CAMPAIGN_DAILY_STAT_REPO
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

.. _dm_class_campaign_daily_stat_repo:

======================
CampaignDailyStatRepo
======================

Repositorio especializado en agregaciones diarias de
``Campaign``. Sigue el mismo patron arquitectonico que
``AgentDailyStatRepo`` pero para la dimension Campaign en
lugar de Agent.

Su responsabilidad es responder consultas pre-agregadas con
granularidad diaria — los reportes de campaign rara vez
necesitan resolucion sub-diaria, asi que la materializacion
diaria reduce coste de query en ordenes de magnitud frente
a leer de la tabla transaccional.

.. uml::
 :caption: Clase CampaignDailyStatRepo — agregaciones
           diarias por Campaign.

 @startuml

 class CampaignDailyStatRepo {
   - storage_backend : StorageBackend
   --
   + aggregate(filters : CampaignFilters, \
               period : DateRange) : List<CampaignDailyStat>
   + top_n(period : DateRange, n : Integer) : List<CampaignDailyStat>
   + total_by_period(period : DateRange) : Map<Date, Integer>
 }

 class CampaignFilters {
   + campaign_id : UUID
   + tenant_id : UUID
   + state : CampaignState
 }

 class CampaignDailyStat {
   + campaign_id : UUID
   + date : Date
   + calls_count : Integer
   + answered_count : Integer
   + abandoned_count : Integer
   + avg_duration_sec : Float
 }

 CampaignDailyStatRepo "1" ..> "0..*" CampaignDailyStat : returns
 CampaignDailyStatRepo "1" ..> "0..*" CampaignFilters : queries with

 @enduml

Operaciones principales
=======================

- ``aggregate(filters, period)`` — agrega estadisticas
  diarias por filtros (campaign, tenant, state) en un rango.
- ``top_n(period, n)`` — top N campaigns por volumen en
  el periodo.
- ``total_by_period(period)`` — totales por dia para
  graficar series temporales.

Restricciones aplicables
========================

- **CNST-025** — las consultas se auditan via
  ``AuditService.emit()`` (responsabilidad del invocante).

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-14/index` —
  ``aggregate``, ``top_n``.

Relaciones
==========

- Es leido por ``CampaignReportService``.
- Materializa agregaciones de ``CallEvent`` y ``Call`` por
  campaign × dia — su carga la realiza el ``Procesador
  Asincrono`` del pipeline ETL.
- No persiste en tiempo real; es read-only desde la
  perspectiva del UC.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/campaign`
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo`
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`
