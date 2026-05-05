.. meta::
 :artefacto: AT_UC_UC_RPT_16
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_rpt_16:

================================
UC_RPT_16 — Reporte de Menus IVR
================================

Diagrama de caso de uso (uml-07) para ``UC_RPT_16``.

.. uml::
 :caption: UC_RPT_16 — Reporte de Menus IVR

 @startuml
 left to right direction

 actor Operator

 rectangle "MOD_Reports" {
   usecase "UC_RPT_16\nReporte de Menus IVR" as UC_RPT_16
 }

 Operator --> UC_RPT_16

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/reports/uc-rpt-16/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/reports/index`.
