.. meta::
 :artefacto: AT_UC_UC_CLI_02
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_cli_02:

=======================
UC_CLI_02 — Navegar IVR
=======================

Diagrama de caso de uso (uml-07) para ``UC_CLI_02``.

.. uml::
 :caption: UC_CLI_02 — Navegar IVR

 @startuml
 left to right direction

 actor Caller

 rectangle "MOD_Caller" {
   usecase "UC_CLI_02\nNavegar IVR" as UC_CLI_02
 }

 Caller --> UC_CLI_02

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/caller/uc-cli-02/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/caller/index`.
