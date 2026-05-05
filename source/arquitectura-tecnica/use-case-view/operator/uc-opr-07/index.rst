.. meta::
 :artefacto: AT_UC_UC_OPR_07
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_opr_07:

===================================
UC_OPR_07 — Solicitar Break / Pausa
===================================

Diagrama de caso de uso (uml-07) para ``UC_OPR_07``.

.. uml::
 :caption: UC_OPR_07 — Solicitar Break / Pausa

 @startuml
 left to right direction

 actor Operator

 rectangle "MOD_Operator" {
   usecase "UC_OPR_07\nSolicitar Break / Pausa" as UC_OPR_07
 }

 Operator --> UC_OPR_07

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/operator/uc-opr-07/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/operator/index`.
