.. meta::
 :artefacto: AT_UC_LOG_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_02_usecase:

=============================================================
UC_LOG_02 — Consultar Logs del ETL: Use Case View
=============================================================

Actores RBAC, relaciones y confines del sistema para UC_LOG_02.

.. uml::
 :caption: UC_LOG_02 — Use Case View

 @startuml

 left to right direction

 actor "view_etl_logs"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nConsultar Logs del ETL" as UCLOG02
 }

 "view_etl_logs" --> UCLOG02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/logs/uc-log-02/actores-precondiciones`
