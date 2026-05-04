.. meta::
 :artefacto: AT_UC_LOG_06_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_06_usecase:

=============================================================
UC_LOG_06 — Ver Estado del Sistema: Use Case View
=============================================================

Actores RBAC, relaciones y confines del sistema para UC_LOG_06.

.. uml::
 :caption: UC_LOG_06 — Use Case View

 @startuml

 left to right direction

 actor "view_system_health"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_06\nVer Estado del Sistema" as UCLOG06
 }

 "view_system_health" --> UCLOG06

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/logs/uc-log-06/actores-precondiciones`
