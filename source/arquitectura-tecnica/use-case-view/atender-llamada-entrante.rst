.. meta::
 :artefacto: AT_UC_OPR_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_02_usecase:

===============================================================
UC_OPR_02 — Atender Llamada Entrante: Use Case View
===============================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_02.

.. uml::
 :caption: UC_OPR_02 — Use Case View

 @startuml

 left to right direction

 actor "answer_inbound_calls"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_02\nAtender Llamada Entrante" as UCOPR02
 }

 "answer_inbound_calls" --> UCOPR02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-02/actores-precondiciones`
