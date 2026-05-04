.. meta::
 :artefacto: AT_UC_RPT_13_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_13_usecase:

=======================================================
UC_RPT_13 — Reporte de Colas: Use Case View
=======================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_13.

.. uml::
 :caption: UC_RPT_13 — Use Case View

 @startuml

 left to right direction

 actor "view_reports"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_13\nReporte de Colas" as UCRPT13
 }

 "view_reports" --> UCRPT13

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-13/actores-precondiciones`
