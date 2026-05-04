.. meta::
 :artefacto: AT_UC_ALR_04_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_04_domain:

===========================================================
UC_ALR_04 — Ver Historial de Alertas: Domain Model
===========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index`.

.. uml::
 :caption: UC_ALR_04 — Domain Model

 @startuml

 left to right direction

 class Alert
 class AlertHistory
 class Alert

 Alert --> AlertHistory
 AlertHistory --> Alert

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index`
