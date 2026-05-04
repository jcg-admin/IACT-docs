.. meta::
 :artefacto: AT_UC_ACC_08_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_08_usecase:

=======================================================
UC_ACC_08 — Permiso Temporal: Use Case View
=======================================================

Actores RBAC, relaciones y confines del sistema para UC_ACC_08.

.. uml::
 :caption: UC_ACC_08 — Use Case View

 @startuml

 left to right direction

 actor "grant_exceptional_permission"

 rectangle "MOD_Access" {
   usecase "UC_ACC_08\nPermiso Temporal" as UCACC08
 }

 "grant_exceptional_permission" --> UCACC08

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/access/uc-acc-08/actores-precondiciones`
