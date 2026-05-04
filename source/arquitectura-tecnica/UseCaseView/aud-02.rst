.. meta::
 :artefacto: AT_UC_AUD_02_UC
 :tipo: Diagrama Arquitectonico — Use Case View
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_02_usecase:

=======================================================
UC_AUD_02 — Buscar Auditoria: Use Case View
=======================================================

Actores RBAC, relaciones y confines del sistema para UC_AUD_02.

.. uml::
 :caption: UC_AUD_02 — Use Case View

 @startuml

 left to right direction

 actor "search_audit_log"

 rectangle "MOD_Audit" {
   usecase "UC_AUD_02\nBuscar Auditoria" as UCAUD02
 }

 "search_audit_log" --> UCAUD02

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/diagramas-uc-por-modulo`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/requisitos/casos-uso/audit/uc-aud-02/actores-precondiciones`
