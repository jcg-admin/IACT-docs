.. meta::
 :artefacto: AT_UC_ACC_01_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_01_usecase:

========================================================
UC_ACC_01 — Asignar Funciones: Use Case View
========================================================

Actores RBAC, relaciones y confines del sistema para UC_ACC_01.

.. uml::
 :caption: UC_ACC_01 — Use Case View

 @startuml

 left to right direction

 actor "assign_functions"

 rectangle "MOD_Access" {
   usecase "UC_ACC_01\nAsignar Funciones" as UCACC01
 }

 "assign_functions" --> UCACC01

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/access/uc-acc-01/actores-precondiciones`
