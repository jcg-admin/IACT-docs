.. meta::
 :artefacto: AT_UC_ALR_01_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_01_impl:

========================================================================
UC_ALR_01 — Configurar Umbrales de Alertas: Implementation View
========================================================================

Componentes y paquetes de codigo que implementan UC_ALR_01.

.. uml::
 :caption: UC_ALR_01 — Implementation View

 @startuml

 package "MOD_Alerts" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/alerts/uc-alr-01/implementacion-tecnica`
