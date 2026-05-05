.. meta::
 :artefacto: AT_UC_UC_CLI_04
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_cli_04:

==============================
UC_CLI_04 — Solicitar Callback
==============================

Diagrama de caso de uso (uml-07) para ``UC_CLI_04``.

.. uml::
 :caption: UC_CLI_04 — Solicitar Callback

 @startuml
 left to right direction

 actor Caller

 rectangle "MOD_Caller" {
   usecase "UC_CLI_04\nSolicitar Callback" as UC_CLI_04
 }

 Caller --> UC_CLI_04

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/caller/uc-cli-04/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/caller/index`.
