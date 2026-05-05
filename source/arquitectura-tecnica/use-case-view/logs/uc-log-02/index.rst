.. meta::
 :artefacto: AT_UC_UC_LOG_02
 :tipo: Diagrama Arquitectonico — UC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_uc_log_02:

==================================
UC_LOG_02 — Consultar Logs del ETL
==================================

Diagrama de caso de uso (uml-07) para ``UC_LOG_02``.

.. uml::
 :caption: UC_LOG_02 — Consultar Logs del ETL

 @startuml
 left to right direction

 actor SystemAdmin

 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nConsultar Logs del ETL" as UC_LOG_02
 }

 SystemAdmin --> UC_LOG_02

 @enduml

Especificación
==============

La especificación completa de este UC vive en:

- :doc:`/requisitos/casos-uso/logs/uc-log-02/index`

Vista de módulo
===============

Para ver este UC en el contexto de todos los UCs del módulo,
ver :doc:`/arquitectura-tecnica/use-case-view/logs/index`.
