.. meta::
 :artefacto: AT_UC_RPT_09_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_09_usecase:

=========================================================
UC_RPT_09 — Configurar Filtros: Use Case View
=========================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_09.

.. uml::
 :caption: UC_RPT_09 — Use Case View

 @startuml

 left to right direction

 actor "filter_reports"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_09\nConfigurar Filtros" as UCRPT09
 }

 "filter_reports" --> UCRPT09

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-09/actores-precondiciones`
