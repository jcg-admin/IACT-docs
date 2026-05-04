.. meta::
 :artefacto: AT_UC_USR_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_01_domain:

================================================
UC_USR_01 — Crear Usuario: Domain Model
================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/users/uc-usr-01/index`.

.. uml::
 :caption: UC_USR_01 — Domain Model

 @startuml

 left to right direction

 class User
 class AccessGroup
 class AuditEvent

 User --> AccessGroup
 AccessGroup --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/users/uc-usr-01/index`
