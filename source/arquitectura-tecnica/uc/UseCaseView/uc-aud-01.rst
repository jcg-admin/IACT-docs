.. meta::
 :artefacto: AT_UC_AUD_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_01_usecase:

==================================================================
UC_AUD_01 — Consultar Auditoria General: Use Case View
==================================================================

Actores RBAC, relaciones y confines del sistema para UC_AUD_01.

.. uml::
 :caption: UC_AUD_01 — Use Case View

 @startuml

 left to right direction

 actor "view_audit_log"

 rectangle "MOD_Audit" {
   usecase "UC_AUD_01\nConsultar Auditoria General" as UCAUD01
 }

 "view_audit_log" --> UCAUD01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/audit/uc-aud-01/actores-precondiciones`
