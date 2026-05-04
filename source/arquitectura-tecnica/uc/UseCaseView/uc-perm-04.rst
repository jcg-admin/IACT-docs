.. meta::
 :artefacto: AT_UC_PERM_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_04_usecase:

===================================================================
UC_PERM_04 — Revocar Permiso Excepcional: Use Case View
===================================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_04.

.. uml::
 :caption: UC_PERM_04 — Use Case View

 @startuml

 left to right direction

 actor "revoke_exceptional_permission"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_04\nRevocar Permiso Excepcional" as UCPERM04
 }

 "revoke_exceptional_permission" --> UCPERM04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-04/actores-precondiciones`
