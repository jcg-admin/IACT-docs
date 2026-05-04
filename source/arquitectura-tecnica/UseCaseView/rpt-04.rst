.. meta::
 :artefacto: AT_UC_RPT_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_04_usecase:

=======================================================
UC_RPT_04 — Exportar Reporte: Use Case View
=======================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_04.

.. uml::
 :caption: UC_RPT_04 — Use Case View

 @startuml

 left to right direction

 actor "export_csv"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_04\nExportar Reporte" as UCRPT04
 }

 "export_csv" --> UCRPT04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-04/actores-precondiciones`
