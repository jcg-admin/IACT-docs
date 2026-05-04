.. meta::
 :artefacto: AT_UC_RPT_17_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_17_usecase:

=================================================================
UC_RPT_17 — Reporte de Clientes Unicos: Use Case View
=================================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_17.

.. uml::
 :caption: UC_RPT_17 — Use Case View

 @startuml

 left to right direction

 actor "view_reports"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_17\nReporte de Clientes Unicos" as UCRPT17
 }

 "view_reports" --> UCRPT17

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-17/actores-precondiciones`
