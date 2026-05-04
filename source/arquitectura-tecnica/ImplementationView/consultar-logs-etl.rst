.. meta::
 :artefacto: AT_UC_LOG_02_IMPL
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_02_impl:

================================================================
UC_LOG_02 — Consultar Logs del ETL: Implementation View
================================================================

Componentes y paquetes de codigo que implementan UC_LOG_02.

.. uml::
 :caption: UC_LOG_02 — Implementation View

 @startuml

 package "MOD_Logs" {
   component "View / Serializer" as ViewSerializer <<api>>
   component "Service / Repository" as ServiceRepo <<service>>
   component "ORM / SP" as ORMLayer <<orm>>
 }

 ViewSerializer --> ServiceRepo : invoca
 ServiceRepo --> ORMLayer : persiste / consulta

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-02/implementacion-tecnica`
