.. meta::
 :artefacto: AT_UC_AUTH_02_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: uc/ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_02_impl:

========================================================
UC_AUTH_02 — Cerrar Sesion: Implementation View
========================================================

Componentes y paquetes de codigo que implementan UC_AUTH_02.

.. uml::
 :caption: UC_AUTH_02 — Implementation View

 @startuml

 package "MOD_Auth" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-02/implementacion-tecnica`
