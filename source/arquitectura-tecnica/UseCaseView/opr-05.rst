.. meta::
 :artefacto: AT_UC_OPR_05_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_05_usecase:

=========================================================
UC_OPR_05 — Transferir Llamada: Use Case View
=========================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_05.

.. uml::
 :caption: UC_OPR_05 — Use Case View

 @startuml

 left to right direction

 actor "transfer_calls"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_05\nTransferir Llamada" as UCOPR05
 }

 "transfer_calls" --> UCOPR05

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-05/actores-precondiciones`
