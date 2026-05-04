.. meta::
 :artefacto: AT_UC_ACC_09_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_09_usecase:

================================================================
UC_ACC_09 — Auditar Cambios de Acceso: Use Case View
================================================================

Actores RBAC, relaciones y confines del sistema para UC_ACC_09.

.. uml::
 :caption: UC_ACC_09 — Use Case View

 @startuml

 left to right direction

 actor "view_audit_log"

 rectangle "MOD_Access" {
   usecase "UC_ACC_09\nAuditar Cambios de Acceso" as UCACC09
 }

 "view_audit_log" --> UCACC09

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/access/uc-acc-09/actores-precondiciones`
