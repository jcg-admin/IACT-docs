.. meta::
 :artefacto: AT_UC_RPT_16_USECASE
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

.. _at_uc_rpt_16_reporte_de_menus_ivr:

============================================================
UC_RPT_16 — Reporte de Menus IVR
============================================================

Identifica cuello de botella en menus IVR: total ingresos, distribucion
por opcion del menu raiz, drop-off rate por nodo, avg time in menu,
top paths. ``view_reports``. Insumo para optimizar IVR.

.. uml::
 :caption: UC_RPT_16 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "IvrNavigationReportService" as IvrNavigationReportService <<sistema>>
 actor "Bucket" as Bucket <<sistema>>
 actor "Call" as Call <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_16\nReporte de Menus IVR" as UC_RPT_16
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Calcular total\ningresos al IVR" as METRIC_VOL
   usecase "Distribucion por\nopcion del menu raiz" as METRIC_DIST
   usecase "Drop-off rate\npor nodo" as METRIC_DROP
   usecase "Avg time in menu\n+ Top paths" as METRIC_PATH
 }

 view_reports --> UC_RPT_16

 UC_RPT_16 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_16 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_16 ..> METRIC_VOL : <<include>>
 UC_RPT_16 ..> METRIC_DIST : <<include>>
 UC_RPT_16 ..> METRIC_DROP : <<include>>
 UC_RPT_16 ..> METRIC_PATH : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 METRIC_VOL --> IvrNavigationReportService
 METRIC_DIST --> Bucket
 METRIC_DROP --> Bucket
 IvrNavigationReportService --> Call

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service` —
   servicio especifico IVR.
 - :doc:`/arquitectura-tecnica/domain-model/base-report-service` —
   patron base.
 - :doc:`/arquitectura-tecnica/domain-model/bucket` —
   distribucion + drop-off.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con paths IVR.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/caller/uc-cli-02/index` —
   UC origen de la navegacion.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-16/index` —
   spec textual.
