.. meta::
 :artefacto: AT_UC_OPR_10_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_10_usecase:

======================================================================
UC_OPR_10 — Recibir Notificacion Supervisor: Use Case View
======================================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_10.

.. uml::
 :caption: UC_OPR_10 — Use Case View

 @startuml

 left to right direction

 actor "read_own_mailbox"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_10\nRecibir Notificacion Supervisor" as UCOPR10
 }

 "read_own_mailbox" --> UCOPR10

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-10/actores-precondiciones`
