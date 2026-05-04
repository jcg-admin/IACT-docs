.. meta::
 :artefacto: AT_UC_SUP_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01_usecase:

=========================================================
UC_SUP_01 — Monitorear Llamada: Use Case View
=========================================================

Actores RBAC, relaciones y confines del sistema para UC_SUP_01.

.. uml::
 :caption: UC_SUP_01 — Use Case View

 @startuml

 left to right direction

 actor "monitor_live_calls"

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitorear Llamada" as UCSUP01
 }

 "monitor_live_calls" --> UCSUP01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/actores-precondiciones`
