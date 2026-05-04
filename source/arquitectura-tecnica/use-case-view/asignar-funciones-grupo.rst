.. meta::
 :artefacto: AT_UC_PERM_06_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_06_usecase:

=================================================================
UC_PERM_06 — Asignar Funciones a Grupo: Use Case View
=================================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_06.

.. uml::
 :caption: UC_PERM_06 — Use Case View

 @startuml

 left to right direction

 actor "assign_functions_to_group"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_06\nAsignar Funciones a Grupo" as UCPERM06
 }

 "assign_functions_to_group" --> UCPERM06

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-06/actores-precondiciones`
