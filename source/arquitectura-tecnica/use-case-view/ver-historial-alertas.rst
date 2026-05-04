.. meta::
 :artefacto: AT_UC_ALR_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_04_usecase:

===============================================================
UC_ALR_04 — Ver Historial de Alertas: Use Case View
===============================================================

Actores RBAC, relaciones y confines del sistema para UC_ALR_04.

.. uml::
 :caption: UC_ALR_04 — Use Case View

 @startuml

 left to right direction

 actor "view_alert_history"

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_04\nVer Historial de Alertas" as UCALR04
 }

 "view_alert_history" --> UCALR04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/actores-precondiciones`
