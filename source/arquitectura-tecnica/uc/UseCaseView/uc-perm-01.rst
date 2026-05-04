.. meta::
 :artefacto: AT_UC_PERM_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_01_usecase:

===============================================================
UC_PERM_01 — Asignar Grupo a Usuario: Use Case View
===============================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_01.

.. uml::
 :caption: UC_PERM_01 — Use Case View

 @startuml

 left to right direction

 actor "assign_function_groups"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_01\nAsignar Grupo a Usuario" as UCPERM01
 }

 "assign_function_groups" --> UCPERM01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-01/actores-precondiciones`
