.. meta::
 :artefacto: AT_UC_UC_AUTH_05
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_auth_05:

===============================
UC_AUTH_05 — Gestionar Sesiones
===============================

Diagrama de caso de uso (uml-07) para ``UC_AUTH_05``.

.. uml::
 :caption: UC_AUTH_05 — Gestionar Sesiones

 @startuml
 left to right direction

 actor AuthUser

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_05\nGestionar Sesiones" as UC_AUTH_05
 }

 AuthUser --> UC_AUTH_05

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/auth/uc-auth-05/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/auth/index`.
