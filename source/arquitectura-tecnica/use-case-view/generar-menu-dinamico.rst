.. meta::
 :artefacto: AT_UC_PERM_08_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_08_usecase:

=============================================================
UC_PERM_08 — Generar Menu Dinamico: Use Case View
=============================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_08.

.. uml::
 :caption: UC_PERM_08 — Use Case View

 @startuml

 left to right direction

 actor "view_assignments"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_08\nGenerar Menu Dinamico" as UCPERM08
 }

 "view_assignments" --> UCPERM08

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-08/actores-precondiciones`
