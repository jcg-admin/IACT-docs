.. meta::
 :artefacto: AT_UC_CLI_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_01_usecase:

=====================================================================
UC_CLI_01 — Iniciar Llamada al Call Center: Use Case View
=====================================================================

Actores RBAC, relaciones y confines del sistema para UC_CLI_01.

.. uml::
 :caption: UC_CLI_01 — Use Case View

 @startuml

 left to right direction

 actor "CallerExterno"

 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nIniciar Llamada al Call Center" as UCCLI01
 }

 "CallerExterno" --> UCCLI01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/caller/uc-cli-01/actores-precondiciones`
