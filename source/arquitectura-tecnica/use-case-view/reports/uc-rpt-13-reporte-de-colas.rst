.. meta::
 :artefacto: AT_UC_RPT_13_USECASE
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

.. _at_uc_rpt_13_reporte_de_colas:

==============================
UC_RPT_13 — Reporte de Colas
==============================

Performance por cola: ASA, SL%, abandono, calls offered/answered, max
wait, queue depth peak. ``view_reports``. Detectar colas saturadas o
con SL bajo.

.. uml::
 :caption: UC_RPT_13 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "BaseReportService" as BaseReportService <<sistema>>
 actor "Bucket" as Bucket <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>
 actor "Call" as Call <<sistema>>
 actor "TimingCalculator" as TimingCalculator <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_13\nReporte de Colas" as UC_RPT_13
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Calcular Calls\noffered/answered/abandoned" as METRIC_VOL
   usecase "Calcular ASA\n(Average Speed of Answer)" as METRIC_ASA
   usecase "Calcular SL %\n(within threshold)" as METRIC_SL
   usecase "Calcular Abandon rate\n+ Max wait + Queue depth" as METRIC_QUEUE
 }

 view_reports --> UC_RPT_13

 UC_RPT_13 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_13 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_13 ..> METRIC_VOL : <<include>>
 UC_RPT_13 ..> METRIC_ASA : <<include>>
 UC_RPT_13 ..> METRIC_SL : <<include>>
 UC_RPT_13 ..> METRIC_QUEUE : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 METRIC_VOL --> BaseReportService
 METRIC_VOL --> Call
 METRIC_ASA --> KpiCalculator
 METRIC_ASA --> TimingCalculator
 METRIC_SL --> KpiCalculator
 METRIC_QUEUE --> Bucket

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron template-method.
 - :doc:`/arquitectura-tecnica/domain-model/bucket` —
   bucket de agregacion.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   ASA, SL, Abandon rate.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   fuente de datos.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   wait times.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-13/index` —
   spec textual.
