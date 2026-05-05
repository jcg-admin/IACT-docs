.. meta::
 :artefacto: AT_UC_RPT_15_USECASE
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

.. _at_uc_rpt_15_reporte_de_transferencias:

==============================
UC_RPT_15 — Reporte de Transferencias
==============================

Identificar patrones de transferencias: total, avg time pre-transfer,
disposition post, top reasons (skill, language, escalation).
``view_reports``. Detectar transfers excesivos (skill misrouting),
circulares, agentes con alta tasa transfer-out.

.. uml::
 :caption: UC_RPT_15 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "TransferReportService" as TransferReportService <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "TimingCalculator" as TimingCalculator <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_15\nReporte de Transferencias" as UC_RPT_15
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Calcular total transfers\n(in/out)" as METRIC_TOTAL
   usecase "Calcular avg time\npre-transfer" as METRIC_PRETIME
   usecase "Calcular Disposition\npost-transfer" as METRIC_POST
   usecase "Top reasons\n(skill, language, escalation)" as METRIC_REASONS
 }

 view_reports --> UC_RPT_15

 UC_RPT_15 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_15 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_15 ..> METRIC_TOTAL : <<include>>
 UC_RPT_15 ..> METRIC_PRETIME : <<include>>
 UC_RPT_15 ..> METRIC_POST : <<include>>
 UC_RPT_15 ..> METRIC_REASONS : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 METRIC_TOTAL --> TransferReportService
 TransferReportService --> Call
 METRIC_PRETIME --> TimingCalculator

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/transfer-report-service` —
   servicio especifico.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron base.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con transferred=true + reason.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   tiempo medio pre-transfer.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-05/index` —
   UC origen de los transfers.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-15/index` —
   spec textual.
