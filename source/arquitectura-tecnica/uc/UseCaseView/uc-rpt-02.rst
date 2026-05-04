.. meta::
 :artefacto: AT_UC_RPT_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_02_usecase:

==================================================================
UC_RPT_02 — Ver Metricas en Tiempo Real: Use Case View
==================================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_02.

.. uml::
 :caption: UC_RPT_02 — Use Case View

 @startuml

 left to right direction

 actor "view_kpis"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_02\nVer Metricas en Tiempo Real" as UCRPT02
 }

 "view_kpis" --> UCRPT02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-02/actores-precondiciones`
