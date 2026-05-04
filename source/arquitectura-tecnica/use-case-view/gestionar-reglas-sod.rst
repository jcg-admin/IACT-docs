.. meta::
 :artefacto: AT_UC_ACC_05_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_05_usecase:

===========================================================
UC_ACC_05 — Gestionar Reglas SoD: Use Case View
===========================================================

Actores RBAC, relaciones y confines del sistema para UC_ACC_05.

.. uml::
 :caption: UC_ACC_05 — Use Case View

 @startuml

 left to right direction

 actor "view_separation_rules"

 rectangle "MOD_Access" {
   usecase "UC_ACC_05\nGestionar Reglas SoD" as UCACC05
 }

 "view_separation_rules" --> UCACC05

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/access/uc-acc-05/actores-precondiciones`
