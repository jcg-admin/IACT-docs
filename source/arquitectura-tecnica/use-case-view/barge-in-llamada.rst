.. meta::
 :artefacto: AT_UC_SUP_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_02_usecase:

==========================================================
UC_SUP_02 — Barge-in en Llamada: Use Case View
==========================================================

Actores RBAC, relaciones y confines del sistema para UC_SUP_02.

.. uml::
 :caption: UC_SUP_02 — Use Case View

 @startuml

 left to right direction

 actor "barge_in_calls"

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_02\nBarge-in en Llamada" as UCSUP02
 }

 "barge_in_calls" --> UCSUP02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-02/actores-precondiciones`
