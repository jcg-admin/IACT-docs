.. meta::
 :artefacto: AT_UC_UC_SUP_01
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_sup_01:

========================================
UC_SUP_01 — Monitorear Llamada (Whisper)
========================================

Diagrama de caso de uso (uml-07) para ``UC_SUP_01``.

.. uml::
 :caption: UC_SUP_01 — Monitorear Llamada (Whisper)

 @startuml
 left to right direction

 actor Supervisor

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamada (Whisper)" as UC_SUP_01
 }

 Supervisor --> UC_SUP_01

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/supervision/uc-sup-01/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/supervision/index`.
