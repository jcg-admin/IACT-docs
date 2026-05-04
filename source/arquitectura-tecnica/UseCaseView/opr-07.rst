.. meta::
 :artefacto: AT_UC_OPR_07_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_07_usecase:

============================================================
UC_OPR_07 — Solicitar Break Pausa: Use Case View
============================================================

Actores RBAC, relaciones y confines del sistema para UC_OPR_07.

.. uml::
 :caption: UC_OPR_07 — Use Case View

 @startuml

 left to right direction

 actor "request_break"

 rectangle "MOD_Operator" {
   usecase "UC_OPR_07\nSolicitar Break Pausa" as UCOPR07
 }

 "request_break" --> UCOPR07

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/operator/uc-opr-07/actores-precondiciones`
