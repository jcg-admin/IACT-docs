.. meta::
 :artefacto: AT_UC_UC_OPR_02
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_opr_02:

====================================
UC_OPR_02 — Atender Llamada Entrante
====================================

Diagrama de caso de uso (uml-07) para ``UC_OPR_02``.

.. uml::
 :caption: UC_OPR_02 — Atender Llamada Entrante

 @startuml
 left to right direction

 actor Operator

 rectangle "MOD_Operator" {
   usecase "UC_OPR_02\nAtender Llamada Entrante" as UC_OPR_02
 }

 Operator --> UC_OPR_02

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/operator/uc-opr-02/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/operator/index`.
