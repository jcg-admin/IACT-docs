.. meta::
 :artefacto: AT_UC_PERM_09_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_09_domain:

==================================================
UC_PERM_09 — Auditar Acceso: Domain Model
==================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/permissions/uc-perm-09/index`.

.. uml::
 :caption: UC_PERM_09 — Domain Model

 @startuml

 left to right direction

 class AuditEvent
 class User
 class Function

 AuditEvent --> User
 User --> Function

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-09/index`
