.. meta::
 :artefacto: AT_UC_ALR_05_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_05_domain:

==========================================================
UC_ALR_05 — Gestionar Suscripciones: Domain Model
==========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/alerts/uc-alr-05/index`.

.. uml::
 :caption: UC_ALR_05 — Domain Model

 @startuml

 left to right direction

 class AlertSubscription
 class AlertConfig
 class User

 AlertSubscription --> AlertConfig
 AlertConfig --> User

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-05/index`
