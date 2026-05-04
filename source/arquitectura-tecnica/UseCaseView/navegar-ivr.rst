.. meta::
 :artefacto: AT_UC_CLI_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_02_usecase:

==================================================
UC_CLI_02 — Navegar IVR: Use Case View
==================================================

Actores RBAC, relaciones y confines del sistema para UC_CLI_02.

.. uml::
 :caption: UC_CLI_02 — Use Case View

 @startuml

 left to right direction

 actor "CallerExterno"

 rectangle "MOD_Caller" {
   usecase "UC_CLI_02\nNavegar IVR" as UCCLI02
 }

 "CallerExterno" --> UCCLI02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/caller/uc-cli-02/actores-precondiciones`
