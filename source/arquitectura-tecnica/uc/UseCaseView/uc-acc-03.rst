.. meta::
 :artefacto: AT_UC_ACC_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_03_usecase:

===================================================================
UC_ACC_03 — Consultar Permisos Efectivos: Use Case View
===================================================================

Actores RBAC, relaciones y confines del sistema para UC_ACC_03.

.. uml::
 :caption: UC_ACC_03 — Use Case View

 @startuml

 left to right direction

 actor "view_assignments"

 rectangle "MOD_Access" {
   usecase "UC_ACC_03\nConsultar Permisos Efectivos" as UCACC03
 }

 "view_assignments" --> UCACC03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/access/uc-acc-03/actores-precondiciones`
