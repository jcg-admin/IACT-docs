.. meta::
 :artefacto: AT_UC_CLI_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_04_usecase:

=========================================================
UC_CLI_04 — Solicitar Callback: Use Case View
=========================================================

Actores RBAC, relaciones y confines del sistema para UC_CLI_04.

.. uml::
 :caption: UC_CLI_04 — Use Case View

 @startuml

 left to right direction

 actor "CallerExterno"

 rectangle "MOD_Caller" {
   usecase "UC_CLI_04\nSolicitar Callback" as UCCLI04
 }

 "CallerExterno" --> UCCLI04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/caller/uc-cli-04/actores-precondiciones`
