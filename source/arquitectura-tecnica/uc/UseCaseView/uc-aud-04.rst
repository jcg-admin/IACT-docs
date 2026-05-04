.. meta::
 :artefacto: AT_UC_AUD_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_04_usecase:

====================================================================
UC_AUD_04 — Generar Reporte de Compliance: Use Case View
====================================================================

Actores RBAC, relaciones y confines del sistema para UC_AUD_04.

.. uml::
 :caption: UC_AUD_04 — Use Case View

 @startuml

 left to right direction

 actor "generate_compliance_report"

 rectangle "MOD_Audit" {
   usecase "UC_AUD_04\nGenerar Reporte de Compliance" as UCAUD04
 }

 "generate_compliance_report" --> UCAUD04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/audit/uc-aud-04/actores-precondiciones`
