.. meta::
 :artefacto: AT_UC_LOG_07_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_07_usecase:

============================================================
UC_LOG_07 — Ver Metricas Tecnicas: Use Case View
============================================================

Actores RBAC, relaciones y confines del sistema para UC_LOG_07.

.. uml::
 :caption: UC_LOG_07 — Use Case View

 @startuml

 left to right direction

 actor "view_technical_metrics"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nVer Metricas Tecnicas" as UCLOG07
 }

 "view_technical_metrics" --> UCLOG07

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/logs/uc-log-07/actores-precondiciones`
