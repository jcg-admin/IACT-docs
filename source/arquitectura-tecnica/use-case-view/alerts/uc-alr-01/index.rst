.. meta::
 :artefacto: AT_UC_UC_ALR_01
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_alr_01:

==========================================
UC_ALR_01 — Configurar Umbrales de Alertas
==========================================

Diagrama de caso de uso (uml-07) para ``UC_ALR_01``.

.. uml::
 :caption: UC_ALR_01 — Configurar Umbrales de Alertas

 @startuml
 left to right direction

 actor Supervisor

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales de Alertas" as UC_ALR_01
 }

 Supervisor --> UC_ALR_01

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/alerts/index`.
