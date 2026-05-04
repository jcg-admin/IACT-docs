.. meta::
 :artefacto: AT_UC_ACC_04_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_04_domain_domain_model:

========================
UC_ACC_04 — Domain Model
========================

UC_ACC_04 — Asignar Agrupador: Domain Model
====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/access/uc-acc-04/index`.

.. uml::
 :caption: UC_ACC_04 — Domain Model

 @startuml

 left to right direction

 class AccessGroup
 class User
 class AuditEvent

 AccessGroup --> User
 User --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/access/uc-acc-04/index`
