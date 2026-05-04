.. meta::
 :artefacto: AT_UC_PERM_04_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_04_domain_domain_model:

=========================
UC_PERM_04 — Domain Model
=========================

UC_PERM_04 — Revocar Permiso Excepcional: Domain Model
===============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/permissions/uc-perm-04/index`.

.. uml::
 :caption: UC_PERM_04 — Domain Model

 @startuml

 left to right direction

 class ExceptionalPermission
 class User
 class AuditEvent

 ExceptionalPermission --> User
 User --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-04/index`
