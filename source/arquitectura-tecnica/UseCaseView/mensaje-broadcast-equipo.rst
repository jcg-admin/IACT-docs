.. meta::
 :artefacto: AT_UC_SUP_03_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_usecase:

==================================================================
UC_SUP_03 — Mensaje Broadcast al Equipo: Use Case View
==================================================================

Actores RBAC, relaciones y confines del sistema para UC_SUP_03.

.. uml::
 :caption: UC_SUP_03 — Use Case View

 @startuml

 left to right direction

 actor "broadcast_team_messages"

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_03\nMensaje Broadcast al Equipo" as UCSUP03
 }

 "broadcast_team_messages" --> UCSUP03

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/actores-precondiciones`
