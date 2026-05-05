.. meta::
 :artefacto: AT_UC_UC_OPR_01
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_opr_01:

=====================================
UC_OPR_01 — Cambiar Estado del Agente
=====================================

Diagrama de caso de uso (uml-07) para ``UC_OPR_01``.

.. uml::
 :caption: UC_OPR_01 — Cambiar Estado del Agente

 @startuml
 left to right direction

 actor Operator

 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado del Agente" as UC_OPR_01
 }

 Operator --> UC_OPR_01

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/operator/uc-opr-01/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/operator/index`.
