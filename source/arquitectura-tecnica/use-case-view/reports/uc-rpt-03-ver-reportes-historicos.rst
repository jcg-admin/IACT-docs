.. meta::
 :artefacto: AT_UC_RPT_03_USECASE
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

.. _at_uc_rpt_03_ver_reportes_historicos:

==============================================
UC_RPT_03 — Ver Reportes Historicos
==============================================

Vista de reportes pre-generados periodicos (diarios, semanales,
mensuales). ``view_reports``. Catalog de HistoricalReport ya
calculados — no calculo en tiempo real.

.. uml::
 :caption: UC_RPT_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_reports" as view_reports
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "HistoricalReport" as HistoricalReport <<sistema>>
 actor "Comparative" as Comparative <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_03\nVer Reportes\nHistoricos" as UC_RPT_03
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Verificar\nview_reports" as VERIFICAR_AGR
   usecase "Listar reportes\npre-generados" as LISTAR
   usecase "Filtrar por period\n(diario|semanal|mensual)" as FILTRAR
   usecase "Comparar periodos" as COMPARAR
 }

 view_reports --> UC_RPT_03

 UC_RPT_03 ..> VERIFICAR_AGR : <<include>>
 UC_RPT_03 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_03 ..> LISTAR : <<include>>
 UC_RPT_03 ..> FILTRAR : <<include>>
 UC_RPT_03 ..> COMPARAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 UC_INC_RPT_01 --> SegmentResolver
 LISTAR --> HistoricalReport
 COMPARAR --> Comparative

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/historical-report` —
   reportes pre-generados.
 - :doc:`/arquitectura-tecnica/domain-model/comparative` —
   comparacion entre periodos.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   isolation.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/reports/uc-rpt-03/index` —
   spec textual.
