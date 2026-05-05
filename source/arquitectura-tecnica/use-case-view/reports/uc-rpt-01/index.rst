.. meta::
 :artefacto: AT_UC_UC_RPT_01
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_rpt_01:

=========================
UC_RPT_01 — Ver Dashboard
=========================

Diagrama de caso de uso (uml-07) para ``UC_RPT_01``.

.. uml::
 :caption: UC_RPT_01 — Ver Dashboard

 @startuml
 left to right direction

 actor Operator

 rectangle "MOD_Reports" {
   usecase "UC_RPT_01\nVer Dashboard" as UC_RPT_01
 }

 Operator --> UC_RPT_01

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/reports/uc-rpt-01/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/reports/index`.
