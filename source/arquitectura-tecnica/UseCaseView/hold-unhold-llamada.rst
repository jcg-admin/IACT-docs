.. meta::
 :artefacto: AT_UC_OPR_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_04_usecase:

==========================================================
UC_OPR_04 — Hold Unhold Llamada: Use Case View
==========================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_04.

.. uml::
 :caption: UC_OPR_04 — Use Case View

 @startuml

 left to right direction

 actor "hold_calls"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_04\nHold Unhold Llamada" as UCOPR04
 }

 "hold_calls" --> UCOPR04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-04/actores-precondiciones`
