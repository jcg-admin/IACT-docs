.. meta::
 :artefacto: AT_UC_RPT_14_USECASE
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

.. _at_uc_rpt_14_reporte_de_campanas:

==============================
UC_RPT_14 — Reporte de Campanas
==============================

Performance por campana (inbound/outbound): contacts attempted/reached,
conversion, calls/hora, TMO, disposition mix. ``view_reports``.
Comparar campanas, identificar mas eficiente.

.. uml::
 :caption: UC_RPT_14 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "BaseReportService" as BaseReportService <<sistema>>
 actor "Campaign" as Campaign <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_14\nReporte de Campanas" as UC_RPT_14
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Calcular Contacts\n(attempted / reached)" as METRIC_CONTACTS
   usecase "Calcular Conversion" as METRIC_CONV
   usecase "Calcular Calls/hora\n+ TMO de campana" as METRIC_TP
   usecase "Calcular Disposition mix" as METRIC_DISP
 }

 view_reports --> UC_RPT_14

 UC_RPT_14 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_14 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_14 ..> METRIC_CONTACTS : <<include>>
 UC_RPT_14 ..> METRIC_CONV : <<include>>
 UC_RPT_14 ..> METRIC_TP : <<include>>
 UC_RPT_14 ..> METRIC_DISP : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 METRIC_CONTACTS --> BaseReportService
 METRIC_CONTACTS --> Campaign
 METRIC_CONTACTS --> Call
 METRIC_CONV --> KpiCalculator
 METRIC_TP --> KpiCalculator

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/campaign` —
   metadata de campanas.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron base.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   Conversion, Calls/hora, TMO.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Calls de la campana.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-14/index` —
   spec textual.
