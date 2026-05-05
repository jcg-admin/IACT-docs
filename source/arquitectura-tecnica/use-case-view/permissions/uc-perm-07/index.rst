.. meta::
 :artefacto: AT_UC_UC_PERM_07
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_perm_07:

=========================================
UC_PERM_07 — Verificar Permiso de Usuario
=========================================

Diagrama de caso de uso (uml-07) para ``UC_PERM_07``.

.. uml::
 :caption: UC_PERM_07 — Verificar Permiso de Usuario

 @startuml
 left to right direction

 actor AccessAdmin

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_07\nVerificar Permiso de Usuario" as UC_PERM_07
 }

 AccessAdmin --> UC_PERM_07

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/permissions/index`.
