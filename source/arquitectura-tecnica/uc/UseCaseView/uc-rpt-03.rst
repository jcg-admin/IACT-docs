.. meta::
 :artefacto: AT_UC_RPT_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_03_usecase:

==============================================================
UC_RPT_03 — Ver Reportes Historicos: Use Case View
==============================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_03.

.. uml::
 :caption: UC_RPT_03 — Use Case View

 @startuml

 left to right direction

 actor "view_reports"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_03\nVer Reportes Historicos" as UCRPT03
 }

 "view_reports" --> UCRPT03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-03/actores-precondiciones`
