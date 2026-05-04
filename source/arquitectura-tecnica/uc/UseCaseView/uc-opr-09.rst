.. meta::
 :artefacto: AT_UC_OPR_09_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: uc/UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_09_usecase:

=======================================================================
UC_OPR_09 — Ver Propio Historial de Llamadas: Use Case View
=======================================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_09.

.. uml::
 :caption: UC_OPR_09 — Use Case View

 @startuml

 left to right direction

 actor "view_own_call_history"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_09\nVer Propio Historial de Llamadas" as UCOPR09
 }

 "view_own_call_history" --> UCOPR09

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-09/actores-precondiciones`
