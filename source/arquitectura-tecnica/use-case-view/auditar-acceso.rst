.. meta::
 :artefacto: AT_UC_PERM_09_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_09_usecase:

======================================================
UC_PERM_09 — Auditar Acceso: Use Case View
======================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_09.

.. uml::
 :caption: UC_PERM_09 — Use Case View

 @startuml

 left to right direction

 actor "view_audit_log"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_09\nAuditar Acceso" as UCPERM09
 }

 "view_audit_log" --> UCPERM09

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-09/actores-precondiciones`
