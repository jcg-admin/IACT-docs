.. meta::
 :artefacto: AT_UC_USR_03_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_03_impl:

===========================================================
UC_USR_03 — Modificar Usuario: Implementation View
===========================================================

Componentes y paquetes de codigo que implementan UC_USR_03.

.. uml::
 :caption: UC_USR_03 — Implementation View

 @startuml

 package "MOD_Users" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-03/implementacion-tecnica`
