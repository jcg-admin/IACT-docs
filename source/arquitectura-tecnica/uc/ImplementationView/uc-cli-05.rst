.. meta::
 :artefacto: AT_UC_CLI_05_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_05_impl:

======================================================================
UC_CLI_05 — Calificar Atencion Post-Call: Implementation View
======================================================================

Componentes y paquetes de codigo que implementan UC_CLI_05.

.. uml::
 :caption: UC_CLI_05 — Implementation View

 @startuml

 package "MOD_Caller" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/caller/uc-cli-05/implementacion-tecnica`
