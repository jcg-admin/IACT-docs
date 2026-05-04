.. meta::
 :artefacto: AT_UC_OPR_09_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_09_impl:

==========================================================================
UC_OPR_09 — Ver Propio Historial de Llamadas: Implementation View
==========================================================================

Componentes y paquetes de codigo que implementan UC_OPR_09.

.. uml::
 :caption: UC_OPR_09 — Implementation View

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

 :doc:`/requisitos/casos-uso/operator/uc-opr-09/implementacion-tecnica`
