.. meta::
 :artefacto: AT_UC_RPT_02_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_rpt_02_ver_metricas_en_tiempo_real:

==============================================
UC_RPT_02 — Ver Metricas en Tiempo Real
==============================================

KPIs streaming con auto-refresh 5-10s. ``view_kpis`` (P-15 separada
de view_reports) — granular para dashboards en pared. Calls offered,
queue depth, agents available, SL real-time.

.. uml::
 :caption: UC_RPT_02 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_kpis" as view_kpis
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>
 actor "MetricsCache" as MetricsCache <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_02\nVer Metricas\nen Tiempo Real" as UC_RPT_02
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_kpis" as VERIFICAR_AGR
   usecase "Cache lookup\n(TTL muy corto)" as CACHE_LOOKUP
   usecase "Calcular KPIs\nstreaming" as CALCULAR
   usecase "Auto-refresh 5s" as REFRESH
 }

 view_kpis --> UC_RPT_02

 UC_RPT_02 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_02 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_02 ..> CACHE_LOOKUP : <<include>>
 UC_RPT_02 ..> CALCULAR : <<include>>
 REFRESH ..> UC_RPT_02 : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 CACHE_LOOKUP --> MetricsCache
 CALCULAR --> KpiCalculator

 note bottom of CACHE_LOOKUP
   TTL muy corto (5-10s) para
   reflejar realidad operacional.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   streaming KPIs.
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache` —
   cache TTL corto.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   isolation.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-02/index` —
   spec textual.
