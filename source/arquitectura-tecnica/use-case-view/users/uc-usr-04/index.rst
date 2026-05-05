.. meta::
 :artefacto: AT_UC_UC_USR_04
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_usr_04:

============================
UC_USR_04 — Eliminar Usuario
============================

Diagrama de caso de uso (uml-07) para ``UC_USR_04``.

.. uml::
 :caption: UC_USR_04 — Eliminar Usuario

 @startuml
 left to right direction

 actor UserAdmin

 rectangle "MOD_Users" {
   usecase "UC_USR_04\nEliminar Usuario" as UC_USR_04
 }

 UserAdmin --> UC_USR_04

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/users/uc-usr-04/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/users/index`.
