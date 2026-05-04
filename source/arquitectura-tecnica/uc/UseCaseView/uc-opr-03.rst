.. meta::
 :artefacto: AT_UC_OPR_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_03_usecase:

================================================================
UC_OPR_03 — Realizar Llamada Saliente: Use Case View
================================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_03.

.. uml::
 :caption: UC_OPR_03 — Use Case View

 @startuml

 left to right direction

 actor "make_outbound_calls"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_03\nRealizar Llamada Saliente" as UCOPR03
 }

 "make_outbound_calls" --> UCOPR03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-03/actores-precondiciones`
