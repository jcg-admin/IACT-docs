.. meta::
 :artefacto: AT_UC_RPT_08_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_08_usecase:

===============================================================
UC_RPT_08 — Ver Reportes Programados: Use Case View
===============================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_08.

.. uml::
 :caption: UC_RPT_08 — Use Case View

 @startuml

 left to right direction

 actor "view_reports"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_08\nVer Reportes Programados" as UCRPT08
 }

 "view_reports" --> UCRPT08

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-08/actores-precondiciones`
