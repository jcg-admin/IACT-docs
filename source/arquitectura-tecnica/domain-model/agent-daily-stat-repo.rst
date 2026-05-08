.. meta::
 :artefacto: AT_DM_CLASS_AGENT_DAILY_STAT_REPO
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

.. _dm_class_agent_daily_stat_repo:

==================
AgentDailyStatRepo
==================

Repositorio de **lectura** de estadísticas diarias por
agente. Las stats las produce el ETL (bounded context
``Pipeline ETL``) consolidando eventos crudos del día en
un registro por ``(agent_id, date)``.

Ofrece dos modos de consulta: agregada (sumatoria sobre
un set de agentes para reportes globales) y por stream
(iteración secuencial sobre las stats de un agente
específico para reportes individuales).

.. uml::
 :caption: Clase AgentDailyStatRepo — repo de lectura
           con agregación + stream.

 @startuml

 class AgentDailyStatRepo {
   - storage_backend : StorageBackend
   --
   + aggregate_by_agent(filters : AgentFilters, period : Period) : List<AgentStats>
   + stream_by_agent(agent_id : UUID, period : Period) : Iterator<AgentDailyStat>
   + get_for_day(agent_id : UUID, day : Date) : AgentDailyStat
   + count_active_days(agent_id : UUID, period : Period) : Integer
   + top_n_by_kpi(kpi_name : String, period : Period, n : Integer) : List<AgentRanking>
 }

 class AgentDailyStat {
   + agent_id : UUID
   + day : Date
   + calls_handled : Integer
   + total_handle_time : Duration
   + total_acw_time : Duration
   + staffed_time : Duration
   + scheduled_time : Duration
 }

 class AgentStats {
   + agent_id : UUID
   + period : Period
   + aggregated_kpis : KPISet
 }

 class AgentRanking {
   + agent_id : UUID
   + rank : Integer
   + value : Double
 }

 class AgentFilters

 AgentDailyStatRepo "1" -- "(agent_id, day)" AgentDailyStat : resolves
 AgentDailyStatRepo "1" ..> "0..*" AgentDailyStat : <<reads>>
 AgentDailyStatRepo "1" ..> "0..*" AgentStats : <<returns>>
 AgentDailyStatRepo "1" ..> "0..*" AgentRanking : <<returns>>

 note right of AgentDailyStatRepo
   Read-only. Las stats se escriben
   por el ETL (bounded context
   Pipeline ETL).
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`
  — reporte de agentes consume ``aggregate_by_agent``
  y ``stream_by_agent``.
- :doc:`/requisitos/casos-uso/operator/uc-opr-08/index`
  — propio dashboard del agente: ``stream_by_agent``
  filtrado a sí mismo.

Relaciones
==========

- Read-only sobre ``AgentDailyStat``.
- Devuelve ``AgentStats`` agregadas y ``AgentRanking``.
- Usado por ``AgentReportService`` (delegación).
