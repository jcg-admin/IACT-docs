.. meta::
 :artefacto: AT_UC_PIP_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_04_usecase:

======================================================================
UC_PIP_04 — Solicitar Reintento de Pipeline: Use Case View
======================================================================

Actores RBAC, relaciones y confines del sistema para UC_PIP_04.

.. uml::
 :caption: UC_PIP_04 — Use Case View

 @startuml

 left to right direction

 actor "request_pipeline_retry"

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_04\nSolicitar Reintento de Pipeline" as UCPIP04
 }

 "request_pipeline_retry" --> UCPIP04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/actores-precondiciones`
