.. meta::
 :artefacto: AT_UC_RPT_11_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_11_usecase:

========================================================
UC_RPT_11 — Compartir Reporte: Use Case View
========================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_11.

.. uml::
 :caption: UC_RPT_11 — Use Case View

 @startuml

 left to right direction

 actor "share_report"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_11\nCompartir Reporte" as UCRPT11
 }

 "share_report" --> UCRPT11

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-11/actores-precondiciones`
