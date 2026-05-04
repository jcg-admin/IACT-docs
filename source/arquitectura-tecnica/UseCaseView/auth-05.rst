.. meta::
 :artefacto: AT_UC_AUTH_05_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_05_usecase:

==========================================================
UC_AUTH_05 — Gestionar Sesiones: Use Case View
==========================================================

Actores RBAC, relaciones y confines del sistema para UC_AUTH_05.

.. uml::
 :caption: UC_AUTH_05 — Use Case View

 @startuml

 left to right direction

 actor "view_own_sessions"

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_05\nGestionar Sesiones" as UCAUTH05
 }

 "view_own_sessions" --> UCAUTH05

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/auth/uc-auth-05/actores-precondiciones`
