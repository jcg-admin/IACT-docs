.. meta::
 :artefacto: AT_UC_PERM_07_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_07_usecase:

====================================================================
UC_PERM_07 — Verificar Permiso de Usuario: Use Case View
====================================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_07.

.. uml::
 :caption: UC_PERM_07 — Use Case View

 @startuml

 left to right direction

 actor "view_assignments"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_07\nVerificar Permiso de Usuario" as UCPERM07
 }

 "view_assignments" --> UCPERM07

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-07/actores-precondiciones`
