.. meta::
 :artefacto: AT_UC_AUTH_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_01_usecase:

======================================================
UC_AUTH_01 — Iniciar Sesion: Use Case View
======================================================

Actores RBAC, relaciones y confines del sistema para UC_AUTH_01.

.. uml::
 :caption: UC_AUTH_01 — Use Case View

 @startuml

 left to right direction

 actor "Usuario"

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_01\nIniciar Sesion" as UCAUTH01
 }

 "Usuario" --> UCAUTH01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/auth/uc-auth-01/actores-precondiciones`
