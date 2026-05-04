.. meta::
 :artefacto: AT_UC_ALR_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_01_domain:

=================================================================
UC_ALR_01 — Configurar Umbrales de Alertas: Domain Model
=================================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index`.

.. uml::
 :caption: UC_ALR_01 — Domain Model

 @startuml

 left to right direction

 class AlertConfig
 class AlertThreshold
 class AuditEvent

 AlertConfig --> AlertThreshold
 AlertThreshold --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-01/index`
