.. meta::
 :artefacto: AT_UC_INC_RPT_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_inc_rpt_01_usecase:

============================================================
UC_INC_RPT_01 — Resolver Segmento: Use Case View
============================================================

Actores RBAC, relaciones y confines del sistema para UC_INC_RPT_01.

.. uml::
 :caption: UC_INC_RPT_01 — Use Case View

 @startuml

 left to right direction

 actor "view_reports"

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as UCINCRPT01
 }

 "view_reports" --> UCINCRPT01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/actores-precondiciones`
