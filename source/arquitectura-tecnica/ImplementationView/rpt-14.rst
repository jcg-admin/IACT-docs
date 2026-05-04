.. meta::
 :artefacto: AT_UC_RPT_14_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_14_impl:

=============================================================
UC_RPT_14 — Reporte de Campanas: Implementation View
=============================================================

Componentes y paquetes de codigo que implementan UC_RPT_14.

.. uml::
 :caption: UC_RPT_14 — Implementation View

 @startuml

 package "MOD_Reports" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-14/implementacion-tecnica`
