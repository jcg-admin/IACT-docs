.. meta::
 :artefacto: AT_UC_AUTH_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_04_usecase:

==========================================================
UC_AUTH_04 — Cambiar Contrasena: Use Case View
==========================================================

Actores RBAC, relaciones y confines del sistema para UC_AUTH_04.

.. uml::
 :caption: UC_AUTH_04 — Use Case View

 @startuml

 left to right direction

 actor "reset_password"

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_04\nCambiar Contrasena" as UCAUTH04
 }

 "reset_password" --> UCAUTH04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/auth/uc-auth-04/actores-precondiciones`
