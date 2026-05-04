.. meta::
 :artefacto: AT_UC_PIP_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_01_usecase:

=====================================================
UC_PIP_01 — Supervisar ETL: Use Case View
=====================================================

Actores RBAC, relaciones y confines del sistema para UC_PIP_01.

.. uml::
 :caption: UC_PIP_01 — Use Case View

 @startuml

 left to right direction

 actor "view_pipeline_status"

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nSupervisar ETL" as UCPIP01
 }

 "view_pipeline_status" --> UCPIP01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/actores-precondiciones`
