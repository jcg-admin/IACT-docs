.. meta::
 :artefacto: AT_UC_PERM_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_02_usecase:

===============================================================
UC_PERM_02 — Revocar Grupo a Usuario: Use Case View
===============================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_02.

.. uml::
 :caption: UC_PERM_02 — Use Case View

 @startuml

 left to right direction

 actor "revoke_function_group"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_02\nRevocar Grupo a Usuario" as UCPERM02
 }

 "revoke_function_group" --> UCPERM02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-02/actores-precondiciones`
