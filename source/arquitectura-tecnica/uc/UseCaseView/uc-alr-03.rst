.. meta::
 :artefacto: AT_UC_ALR_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_03_usecase:

=======================================================
UC_ALR_03 — Reconocer Alerta: Use Case View
=======================================================

Actores RBAC, relaciones y confines del sistema para UC_ALR_03.

.. uml::
 :caption: UC_ALR_03 — Use Case View

 @startuml

 left to right direction

 actor "acknowledge_alert"

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_03\nReconocer Alerta" as UCALR03
 }

 "acknowledge_alert" --> UCALR03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-03/actores-precondiciones`
