.. meta::
 :artefacto: AT_UC_UC_INC_RPT_01
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_inc_rpt_01:

=================================
UC_INC_RPT_01 — Resolver Segmento
=================================

Diagrama de caso de uso (uml-07) para ``UC_INC_RPT_01``.

.. uml::
 :caption: UC_INC_RPT_01 — UC_INC_RPT_01 — Resolver Segmento

 @startuml
 left to right direction

 actor Operator

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nUC_INC_RPT_01 — Resolver Segmento" as UC_INC_RPT_01
 }

 Operator --> UC_INC_RPT_01

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/reports/index`.
