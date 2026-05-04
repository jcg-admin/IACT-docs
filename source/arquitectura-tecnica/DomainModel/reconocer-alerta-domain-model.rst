.. meta::
 :artefacto: AT_UC_ALR_03_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_03_domain_domain_model:

========================
UC_ALR_03 — Domain Model
========================

UC_ALR_03 — Reconocer Alerta: Domain Model
===================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index`.

.. uml::
 :caption: UC_ALR_03 — Domain Model

 @startuml

 left to right direction

 class Alert
 class AuditEvent
 class Alert

 Alert --> AuditEvent
 AuditEvent --> Alert

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index`
