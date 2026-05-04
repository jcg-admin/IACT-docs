.. meta::
 :artefacto: AT_UC_SUP_03_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_impl:

=====================================================================
UC_SUP_03 — Mensaje Broadcast al Equipo: Implementation View
=====================================================================

Componentes y paquetes de codigo que implementan UC_SUP_03.

.. uml::
 :caption: UC_SUP_03 — Implementation View

 @startuml

 package "MOD_Supervision" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/implementacion-tecnica`
