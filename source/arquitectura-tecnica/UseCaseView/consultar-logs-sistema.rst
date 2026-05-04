.. meta::
 :artefacto: AT_UC_LOG_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_01_usecase:

=================================================================
UC_LOG_01 — Consultar Logs del Sistema: Use Case View
=================================================================

Actores RBAC, relaciones y confines del sistema para UC_LOG_01.

.. uml::
 :caption: UC_LOG_01 — Use Case View

 @startuml

 left to right direction

 actor "view_application_logs"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nConsultar Logs del Sistema" as UCLOG01
 }

 "view_application_logs" --> UCLOG01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/logs/uc-log-01/actores-precondiciones`
