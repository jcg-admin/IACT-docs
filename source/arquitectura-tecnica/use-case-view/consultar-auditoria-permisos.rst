.. meta::
 :artefacto: AT_UC_PERM_10_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_10_usecase:

=======================================================================
UC_PERM_10 — Consultar Auditoria de Permisos: Use Case View
=======================================================================

Actores RBAC, relaciones y confines del sistema para UC_PERM_10.

.. uml::
 :caption: UC_PERM_10 — Use Case View

 @startuml

 left to right direction

 actor "view_audit_log"

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_10\nConsultar Auditoria de Permisos" as UCPERM10
 }

 "view_audit_log" --> UCPERM10

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-10/actores-precondiciones`
