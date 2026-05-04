.. meta::
 :artefacto: AT_UC_ALR_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_01_usecase:

=====================================================================
UC_ALR_01 — Configurar Umbrales de Alertas: Use Case View
=====================================================================

Actores RBAC, relaciones y confines del sistema para UC_ALR_01.

.. uml::
 :caption: UC_ALR_01 — Use Case View

 @startuml

 left to right direction

 actor "configure_alerts"

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales de Alertas" as UCALR01
 }

 "configure_alerts" --> UCALR01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-01/actores-precondiciones`
