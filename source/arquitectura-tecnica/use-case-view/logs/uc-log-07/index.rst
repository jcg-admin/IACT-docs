.. meta::
 :artefacto: AT_UC_UC_LOG_07
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_log_07:

=================================
UC_LOG_07 — Ver Metricas Tecnicas
=================================

Diagrama de caso de uso (uml-07) para ``UC_LOG_07``.

.. uml::
 :caption: UC_LOG_07 — Ver Metricas Tecnicas

 @startuml
 left to right direction

 actor SystemAdmin

 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nVer Metricas Tecnicas" as UC_LOG_07
 }

 SystemAdmin --> UC_LOG_07

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/logs/uc-log-07/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/logs/index`.
