.. meta::
 :artefacto: AT_UC_UC_RPT_15
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_rpt_15:

=====================================
UC_RPT_15 — Reporte de Transferencias
=====================================

Diagrama de caso de uso (uml-07) para ``UC_RPT_15``.

.. uml::
 :caption: UC_RPT_15 — Reporte de Transferencias

 @startuml
 left to right direction

 actor Operator

 rectangle "MOD_Reports" {
   usecase "UC_RPT_15\nReporte de Transferencias" as UC_RPT_15
 }

 Operator --> UC_RPT_15

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/reports/uc-rpt-15/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/reports/index`.
