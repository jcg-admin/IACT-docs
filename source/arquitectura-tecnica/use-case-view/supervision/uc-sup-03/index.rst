.. meta::
 :artefacto: AT_UC_UC_SUP_03
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_sup_03:

=======================================
UC_SUP_03 — Mensaje Broadcast al Equipo
=======================================

Diagrama de caso de uso (uml-07) para ``UC_SUP_03``.

.. uml::
 :caption: UC_SUP_03 — Mensaje Broadcast al Equipo

 @startuml
 left to right direction

 actor Supervisor

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_03\nMensaje Broadcast al Equipo" as UC_SUP_03
 }

 Supervisor --> UC_SUP_03

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/supervision/index`.
