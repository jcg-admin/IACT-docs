.. meta::
 :artefacto: AT_UC_OPR_08_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_08_usecase:

===========================================================
UC_OPR_08 — Ver Propio Dashboard: Use Case View
===========================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_08.

.. uml::
 :caption: UC_OPR_08 — Use Case View

 @startuml

 left to right direction

 actor "view_own_performance_dashboard"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_08\nVer Propio Dashboard" as UCOPR08
 }

 "view_own_performance_dashboard" --> UCOPR08

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-08/actores-precondiciones`
