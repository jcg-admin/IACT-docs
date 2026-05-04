.. meta::
 :artefacto: AT_UC_USR_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_04_usecase:

=======================================================
UC_USR_04 — Eliminar Usuario: Use Case View
=======================================================

Actores RBAC, relaciones y confines del sistema para UC_USR_04.

.. uml::
 :caption: UC_USR_04 — Use Case View

 @startuml

 left to right direction

 actor "deactivate_users"

 rectangle "MOD_Users" {
   usecase "UC_USR_04\nEliminar Usuario" as UCUSR04
 }

 "deactivate_users" --> UCUSR04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/users/uc-usr-04/actores-precondiciones`
