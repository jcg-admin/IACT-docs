.. meta::
 :artefacto: AT_UC_AUTH_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_02_usecase:

=====================================================
UC_AUTH_02 — Cerrar Sesion: Use Case View
=====================================================

Actores RBAC, relaciones y confines del sistema para UC_AUTH_02.

.. uml::
 :caption: UC_AUTH_02 — Use Case View

 @startuml

 left to right direction

 actor "close_user_session"

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_02\nCerrar Sesion" as UCAUTH02
 }

 "close_user_session" --> UCAUTH02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/auth/uc-auth-02/actores-precondiciones`
