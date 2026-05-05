.. meta::
 :artefacto: AT_UC_UC_AUTH_03
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_auth_03:

=================================
UC_AUTH_03 — Recuperar Contrasena
=================================

Diagrama de caso de uso (uml-07) para ``UC_AUTH_03``.

.. uml::
 :caption: UC_AUTH_03 — Recuperar Contrasena

 @startuml
 left to right direction

 actor AuthUser

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_03\nRecuperar Contrasena" as UC_AUTH_03
 }

 AuthUser --> UC_AUTH_03

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/auth/uc-auth-03/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/auth/index`.
