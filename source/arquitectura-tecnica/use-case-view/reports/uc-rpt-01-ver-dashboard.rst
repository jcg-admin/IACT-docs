.. meta::
 :artefacto: AT_UC_RPT_01_USECASE
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

.. _at_uc_rpt_01_ver_dashboard:

==============================
UC_RPT_01 — Ver Dashboard
==============================

Dashboard general operacional con KPIs en tiempo real (calls offered,
ASA, SL, abandon rate). ``view_reports`` + UC_INC_RPT_01 included.
Auto-refresh 30s. CNST-007 read-only Analytics.

.. uml::
 :caption: UC_RPT_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "BaseReportService" as BaseReportService <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>
 actor "MetricsCache" as MetricsCache <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_01\nVer Dashboard" as UC_RPT_01
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Cache lookup" as CACHE_LOOKUP
   usecase "Calcular KPIs\nen tiempo real" as CALCULAR
   usecase "Auto-refresh 30s" as REFRESH
 }

 view_reports --> UC_RPT_01

 UC_RPT_01 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_01 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_01 ..> CACHE_LOOKUP : <<include>>
 UC_RPT_01 ..> CALCULAR : <<include>>
 REFRESH ..> UC_RPT_01 : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 CACHE_LOOKUP --> MetricsCache
 CALCULAR --> KpiCalculator
 KpiCalculator --> BaseReportService

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   calculo KPIs.
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache` —
   cache TTL.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   isolation.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-01/index` —
   spec textual.
