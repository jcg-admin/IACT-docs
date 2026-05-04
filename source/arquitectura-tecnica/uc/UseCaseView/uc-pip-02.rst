.. meta::
 :artefacto: AT_UC_PIP_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_02_usecase:

============================================================
UC_PIP_02 — Consultar Errores ETL: Use Case View
============================================================

Actores RBAC, relaciones y confines del sistema para UC_PIP_02.

.. uml::
 :caption: UC_PIP_02 — Use Case View

 @startuml

 left to right direction

 actor "view_pipeline_errors"

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_02\nConsultar Errores ETL" as UCPIP02
 }

 "view_pipeline_errors" --> UCPIP02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/actores-precondiciones`
