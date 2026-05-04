.. meta::
 :artefacto: AT_UC_AUD_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_03_usecase:

=========================================================
UC_AUD_03 — Exportar Auditoria: Use Case View
=========================================================

Actores RBAC, relaciones y confines del sistema para UC_AUD_03.

.. uml::
 :caption: UC_AUD_03 — Use Case View

 @startuml

 left to right direction

 actor "export_audit_log"

 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Auditoria" as UCAUD03
 }

 "export_audit_log" --> UCAUD03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/audit/uc-aud-03/actores-precondiciones`
