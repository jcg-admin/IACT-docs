.. meta::
 :artefacto: AT_UC_INC_RPT_01_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_inc_rpt_01_impl:

===============================================================
UC_INC_RPT_01 — Resolver Segmento: Implementation View
===============================================================

Componentes y paquetes de codigo que implementan UC_INC_RPT_01.

.. uml::
 :caption: UC_INC_RPT_01 — Implementation View

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

 :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/implementacion-tecnica`
