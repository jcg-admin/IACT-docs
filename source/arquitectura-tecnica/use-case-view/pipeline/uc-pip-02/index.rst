.. meta::
 :artefacto: AT_UC_UC_PIP_02
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_pip_02:

=================================
UC_PIP_02 — Consultar Errores ETL
=================================

Diagrama de caso de uso (uml-07) para ``UC_PIP_02``.

.. uml::
 :caption: UC_PIP_02 — Consultar Errores ETL

 @startuml
 left to right direction

 actor PipelineAdmin

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_02\nConsultar Errores ETL" as UC_PIP_02
 }

 PipelineAdmin --> UC_PIP_02

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/pipeline/index`.
