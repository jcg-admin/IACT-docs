.. meta::
 :artefacto: AT_UC_UC_ACC_05
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_acc_05:

================================
UC_ACC_05 — Gestionar Reglas SoD
================================

Diagrama de caso de uso (uml-07) para ``UC_ACC_05``.

.. uml::
 :caption: UC_ACC_05 — Gestionar Reglas SoD

 @startuml
 left to right direction

 actor AccessAdmin

 rectangle "MOD_Access" {
   usecase "UC_ACC_05\nGestionar Reglas SoD" as UC_ACC_05
 }

 AccessAdmin --> UC_ACC_05

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/access/uc-acc-05/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/access/index`.
