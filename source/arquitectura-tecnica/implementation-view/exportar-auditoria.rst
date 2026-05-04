.. meta::
 :artefacto: AT_UC_AUD_03_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_03_impl:

============================================================
UC_AUD_03 — Exportar Auditoria: Implementation View
============================================================

Componentes y paquetes de codigo que implementan UC_AUD_03.

.. uml::
 :caption: UC_AUD_03 — Implementation View

 @startuml

 package "MOD_Audit" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/audit/uc-aud-03/implementacion-tecnica`
