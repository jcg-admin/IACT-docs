.. meta::
 :artefacto: AT_UC_PERM_05_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_05_usecase:

===============================================================
UC_PERM_05 — Crear Grupo de Permisos: Use Case View
===============================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_05.

.. uml::
 :caption: UC_PERM_05 — Use Case View

 @startuml

 left to right direction

 actor "create_function_group"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_05\nCrear Grupo de Permisos" as UCPERM05
 }

 "create_function_group" --> UCPERM05

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-05/actores-precondiciones`
