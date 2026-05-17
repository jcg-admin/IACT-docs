.. meta::
 :artefacto: AT_UC_RPT_12_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_rpt_12_reporte_de_agentes:

================================
UC_RPT_12 — Reporte de Agentes
================================

Reporte agregado de productividad y performance por agente del segmento
del invoker. Casos de uso: revision semanal de KPIs (TMO, AHT,
ocupacion, adherence), identificar gaps de capacitacion, balanceo de
cargas. Vista detallada por agente disponible con funcion adicional
``view_agent_detail`` (audit reforzado P-44).

.. uml::
 :caption: UC_RPT_12 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "view_agent_detail" as view_agent_detail <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "AgentReportService" as AgentReportService <<sistema>>
 actor "AgentDailyStatRepo" as AgentDailyStatRepo <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>
 actor "MetricsCache" as MetricsCache <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_12\nReporte de Agentes\n.. extension points ..\nDetalleAgente" as UC_RPT_12
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Validar params\n(period, filters)" as VALIDAR_PARAMS
   usecase "Lookup MetricsCache" as CACHE_LOOKUP
   usecase "Query AgentDailyStat\nagregado por periodo" as QUERY_REPO
   usecase "Calcular KPIs\n(TMO/AHT/Occupancy/\nAdherence)" as CALCULAR_KPIS
   usecase "Construir summary\ndel team" as CONSTRUIR_SUMMARY
   usecase "Write cache\nTTL adaptativo" as CACHE_WRITE
   usecase "Detalle por agente\n(audit reforzado P-44)" as DETALLE_AGENTE
 }

 view_reports --> UC_RPT_12
 view_agent_detail --> DETALLE_AGENTE

 UC_RPT_12 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_12 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_12 ..> VALIDAR_PARAMS : <<include>>
 UC_RPT_12 ..> CACHE_LOOKUP : <<include>>
 UC_RPT_12 ..> QUERY_REPO : <<include>>
 UC_RPT_12 ..> CALCULAR_KPIS : <<include>>
 UC_RPT_12 ..> CONSTRUIR_SUMMARY : <<include>>
 UC_RPT_12 ..> CACHE_WRITE : <<include>>
 DETALLE_AGENTE ..> UC_RPT_12 : <<extend>> (DetalleAgente)

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 QUERY_REPO --> AgentReportService
 AgentReportService --> AgentDailyStatRepo
 CALCULAR_KPIS --> KpiCalculator
 CACHE_LOOKUP --> MetricsCache
 CACHE_WRITE --> MetricsCache
 DETALLE_AGENTE --> AuditService
 AuditService --> view_audit_log

 note bottom of UC_INC_RPT_01
   Resuelve segmentos accesibles
   del User (CNST-008 isolation).
   Out-of-segment retorna vacio.
 end note

 note bottom of CACHE_LOOKUP
   TTL adaptativo via MetricsCache:
   5 min para periodo en vivo,
   1h para historicas.
 end note

 note bottom of DETALLE_AGENTE
   Funcion separada view_agent_detail
   con audit reforzado P-44 —
   ver datos individuales
   incrementa criticidad.
 end note

 @enduml

.. seealso::

 **Domain-model entities** referenciadas:

 - :doc:`/arquitectura-tecnica/domain-model/agent-report-service` —
   servicio que orquesta el reporte de agentes.
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo` —
   repositorio de stats diarias agregadas.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method base de los report services.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   componente de calculo de KPIs (TMO/AHT/Occupancy/Adherence).
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache` —
   cache TTL adaptativo de KPIs agregados.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   resolver de segmentos via UC_INC_RPT_01.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica view_reports / view_agent_detail.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor de AGENT_DETAIL_VIEWED (P-44 reforzado).
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   KpiAggregationStrategy variants (avg/p95/p99).

 **UC backing del segment resolver**:

 - :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index` —
   UC de inclusion (no standalone).

 **Spec textual** del UC:

 - :doc:`/requisitos/casos-uso/reports/uc-rpt-12/index` — Parte 1-12.
