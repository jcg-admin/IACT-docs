.. meta::
 :artefacto: AT_UC_OPR_10_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_10_impl:

=========================================================================
UC_OPR_10 — Recibir Notificacion Supervisor: Implementation View
=========================================================================

Componentes y paquetes de codigo que implementan UC_OPR_10.

.. uml::
 :caption: UC_OPR_10 — Implementation View

 @startuml

 package "MOD_Operator" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-10/implementacion-tecnica`
