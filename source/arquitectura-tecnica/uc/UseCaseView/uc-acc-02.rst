.. meta::
 :artefacto: AT_UC_ACC_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_02_usecase:

========================================================
UC_ACC_02 — Revocar Funciones: Use Case View
========================================================

Actores RBAC, relaciones y confines del sistema para UC_ACC_02.

.. uml::
 :caption: UC_ACC_02 — Use Case View

 @startuml

 left to right direction

 actor "revoke_functions"

 rectangle "MOD_Access" {
   usecase "UC_ACC_02\nRevocar Funciones" as UCACC02
 }

 "revoke_functions" --> UCACC02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/access/uc-acc-02/actores-precondiciones`
