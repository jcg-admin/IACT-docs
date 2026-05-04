.. meta::
 :artefacto: AT_UC_LOG_05_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_05_usecase:

==================================================================
UC_LOG_05 — Ver Logs de Infraestructura: Use Case View
==================================================================

Actores RBAC, relaciones y confines del sistema para UC_LOG_05.

.. uml::
 :caption: UC_LOG_05 — Use Case View

 @startuml

 left to right direction

 actor "view_infrastructure_logs"

 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nVer Logs de Infraestructura" as UCLOG05
 }

 "view_infrastructure_logs" --> UCLOG05

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/logs/uc-log-05/actores-precondiciones`
