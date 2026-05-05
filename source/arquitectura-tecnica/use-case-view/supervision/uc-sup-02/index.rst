.. meta::
 :artefacto: AT_UC_UC_SUP_02
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_sup_02:

===============================
UC_SUP_02 — Barge-in en Llamada
===============================

Diagrama de caso de uso (uml-07) para ``UC_SUP_02``.

.. uml::
 :caption: UC_SUP_02 — Barge-in en Llamada

 @startuml
 left to right direction

 actor Supervisor

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_02\nBarge-in en Llamada" as UC_SUP_02
 }

 Supervisor --> UC_SUP_02

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/supervision/uc-sup-02/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/supervision/index`.
