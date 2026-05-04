.. meta::
 :artefacto: AT_UC_USR_04_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_04_domain_domain_model:

========================
UC_USR_04 — Domain Model
========================

UC_USR_04 — Eliminar Usuario: Domain Model
===================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/users/uc-usr-04/index`.

.. uml::
 :caption: UC_USR_04 — Domain Model

 @startuml

 left to right direction

 class User
 class AuditEvent
 class User

 User --> AuditEvent
 AuditEvent --> User

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/users/uc-usr-04/index`
