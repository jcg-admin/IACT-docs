.. meta::
 :artefacto: AT_UC_PIP_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_03_usecase:

========================================================================
UC_PIP_03 — Consultar Disponibilidad de Datos: Use Case View
========================================================================

Actores RBAC, relaciones y confines del sistema para UC_PIP_03.

.. uml::
 :caption: UC_PIP_03 — Use Case View

 @startuml

 left to right direction

 actor "view_data_availability"

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_03\nConsultar Disponibilidad de Datos" as UCPIP03
 }

 "view_data_availability" --> UCPIP03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/actores-precondiciones`
