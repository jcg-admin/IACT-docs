.. meta::
 :artefacto: AT_DM_CLASS_AGENT_REPORT_SERVICE
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

.. _dm_class_agent_report_service:

==================
AgentReportService
==================

Servicio de aplicación que orquesta la **generación de
reportes de agentes**: consume ``AgentDailyStatRepo``,
calcula KPIs derivados con ``KPICalculator`` y retorna un
``HistoricalReport`` con buckets por agente.

Aplica filtros de segmento (CNST-008) vía
``SegmentResolver`` antes de consultar el repo.

.. uml::
 :caption: Clase AgentReportService — orquestador del
           reporte de agentes con filtrado por segmento.

 @startuml

 abstract class BaseReportService

 class AgentReportService {
   --
   + get(invoker : User, period : Period, \
         filters : AgentFilters) : HistoricalReport
   + detail(invoker : User, agent_id : UUID, period : Period) : AgentDetailReport
   + top_performers(invoker : User, kpi_name : String, \
                     period : Period, n : Integer) : List<AgentRanking>
 }

 class AgentDetailReport {
   + agent_id : UUID
   + period : Period
   + kpis : KPISet
   + daily_breakdown : List<Bucket>
   + comparative : Comparative
 }

 class AgentDailyStatRepo
 class HistoricalReport
 class AgentRanking

 BaseReportService <|-- AgentReportService

 AgentReportService "1" o-- "1" AgentDailyStatRepo : reads
 AgentReportService "1" ..> "1" HistoricalReport : <<returns>>
 AgentReportService "1" ..> "0..1" AgentDetailReport : <<returns>>
 AgentReportService "1" ..> "0..*" AgentRanking : <<returns>>

 note bottom of AgentDetailReport
   daily_breakdown : {ordered}
 end note

 note right of AgentReportService
   Hereda atributos protegidos y
   apply_segment_filter de
   BaseReportService (template-method).
 end note

 @enduml

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index`
  — UC principal de reporte de agentes.
- :doc:`/requisitos/casos-uso/operator/uc-opr-08/index`
  — propio dashboard del agente vía ``detail`` filtrado.

Relaciones
==========

- Agregación con ``AgentDailyStatRepo`` y
  ``SegmentResolver`` (servicios externos).
- Composición con ``KPICalculator`` (componente puro).
- Devuelve ``HistoricalReport`` y ``AgentDetailReport``.
