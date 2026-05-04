.. meta::
 :artefacto: AT_UC_ACC_04_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_04_usecase:

========================================================
UC_ACC_04 — Asignar Agrupador: Use Case View
========================================================

Actores RBAC, relaciones y confines del sistema para UC_ACC_04.

.. uml::
 :caption: UC_ACC_04 — Use Case View

 @startuml

 left to right direction

 actor "assign_function_groups"

 rectangle "MOD_Access" {
   usecase "UC_ACC_04\nAsignar Agrupador" as UCACC04
 }

 "assign_function_groups" --> UCACC04

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/access/uc-acc-04/actores-precondiciones`
