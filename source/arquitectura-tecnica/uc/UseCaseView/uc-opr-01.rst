.. meta::
 :artefacto: AT_UC_OPR_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_01_usecase:

================================================================
UC_OPR_01 — Cambiar Estado del Agente: Use Case View
================================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_01.

.. uml::
 :caption: UC_OPR_01 — Use Case View

 @startuml

 left to right direction

 actor "manage_own_agent_state"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado del Agente" as UCOPR01
 }

 "manage_own_agent_state" --> UCOPR01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-01/actores-precondiciones`
