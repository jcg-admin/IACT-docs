.. meta::
 :artefacto: AT_UC_RPT_10_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_10_usecase:

====================================================
UC_RPT_10 — Guardar Vista: Use Case View
====================================================

Actores RBAC, relaciones y confines del sistema para UC_RPT_10.

.. uml::
 :caption: UC_RPT_10 — Use Case View

 @startuml

 left to right direction

 actor "save_view"

 rectangle "MOD_Reports" {
   usecase "UC_RPT_10\nGuardar Vista" as UCRPT10
 }

 "save_view" --> UCRPT10

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/reports/uc-rpt-10/actores-precondiciones`
