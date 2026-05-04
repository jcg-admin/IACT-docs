.. meta::
 :artefacto: AT_UC_LOG_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_04_usecase:

====================================================
UC_LOG_04 — Exportar Logs: Use Case View
====================================================

Actores RBAC, relaciones y confines del sistema para UC_LOG_04.

.. uml::
 :caption: UC_LOG_04 — Use Case View

 @startuml

 left to right direction

 actor "export_logs"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExportar Logs" as UCLOG04
 }

 "export_logs" --> UCLOG04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/logs/uc-log-04/actores-precondiciones`
