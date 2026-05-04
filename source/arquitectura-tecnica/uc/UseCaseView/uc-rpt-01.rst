.. meta::
 :artefacto: AT_UC_RPT_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_01_usecase:

====================================================
UC_RPT_01 — Ver Dashboard: Use Case View
====================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_01.

.. uml::
 :caption: UC_RPT_01 — Use Case View

 @startuml

 left to right direction

 actor "view_dashboard"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_01\nVer Dashboard" as UCRPT01
 }

 "view_dashboard" --> UCRPT01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-01/actores-precondiciones`
