.. meta::
 :artefacto: AT_UC_PERM_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_03_usecase:

====================================================================
UC_PERM_03 — Conceder Permiso Excepcional: Use Case View
====================================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_03.

.. uml::
 :caption: UC_PERM_03 — Use Case View

 @startuml

 left to right direction

 actor "grant_exceptional_permission"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_03\nConceder Permiso Excepcional" as UCPERM03
 }

 "grant_exceptional_permission" --> UCPERM03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-03/actores-precondiciones`
