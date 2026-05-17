.. meta::
 :artefacto: AT_UC_RPT_17_USECASE
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

.. _at_uc_rpt_17_reporte_de_clientes_unicos:

============================================================
UC_RPT_17 — Reporte de Clientes Unicos
============================================================

Mide alcance: cuantos clientes distintos contactaron, recurrencia,
distribucion de frecuencia. ``view_reports``. CNST-026 sin PII —
identificador via hash de telefono/cliente_id.

.. uml::
 :caption: UC_RPT_17 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "CallerReportService" as CallerReportService <<sistema>>
 actor "Sanitizer" as Sanitizer <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_17\nReporte de\nClientes Unicos" as UC_RPT_17
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Hashear caller_id\n(CNST-026)" as HASH
   usecase "Calcular clientes\ndistintos" as METRIC_UNIQUE
   usecase "Calcular recurrencia\n(distribucion)" as METRIC_RECUR
 }

 view_reports --> UC_RPT_17

 UC_RPT_17 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_17 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_17 ..> HASH : <<include>>
 UC_RPT_17 ..> METRIC_UNIQUE : <<include>>
 UC_RPT_17 ..> METRIC_RECUR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 HASH --> Sanitizer
 METRIC_UNIQUE --> CallerReportService
 METRIC_RECUR --> KpiCalculator
 CallerReportService --> Call

 note bottom of HASH
   CNST-026 sin PII: identificador
   via hash del telefono o cliente_id.
   NUNCA valor en limpio.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/caller-report-service` —
   servicio especifico clientes unicos.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron base.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   hashea caller_id.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Calls con caller_hash.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   distribucion recurrencia.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-17/index` —
   spec textual.
