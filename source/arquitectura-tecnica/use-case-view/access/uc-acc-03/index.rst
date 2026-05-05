.. meta::
 :artefacto: AT_UC_UC_ACC_03
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_acc_03:

========================================
UC_ACC_03 — Consultar Permisos Efectivos
========================================

Diagrama de caso de uso (uml-07) para ``UC_ACC_03``.

.. uml::
 :caption: UC_ACC_03 — Consultar Permisos Efectivos

 @startuml
 left to right direction

 actor AccessAdmin

 rectangle "MOD_Access" {
   usecase "UC_ACC_03\nConsultar Permisos Efectivos" as UC_ACC_03
 }

 AccessAdmin --> UC_ACC_03

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/access/uc-acc-03/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/access/index`.
