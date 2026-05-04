.. meta::
 :artefacto: AT_UC_PERM_10_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_10_impl:

==========================================================================
UC_PERM_10 — Consultar Auditoria de Permisos: Implementation View
==========================================================================

Componentes y paquetes de codigo que implementan UC_PERM_10.

.. uml::
 :caption: UC_PERM_10 — Implementation View

 @startuml

 package "MOD_Permissions" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-10/implementacion-tecnica`
