.. meta::
 :artefacto: AT_UC_OPR_06_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_06_usecase:

===========================================================
UC_OPR_06 — Ingresar Disposition: Use Case View
===========================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_06.

.. uml::
 :caption: UC_OPR_06 — Use Case View

 @startuml

 left to right direction

 actor "enter_call_disposition"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_06\nIngresar Disposition" as UCOPR06
 }

 "enter_call_disposition" --> UCOPR06

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-06/actores-precondiciones`
