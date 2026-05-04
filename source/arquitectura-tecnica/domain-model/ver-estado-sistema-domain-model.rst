.. meta::
 :artefacto: AT_UC_LOG_06_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_06_domain_domain_model:

========================
UC_LOG_06 — Domain Model
========================

UC_LOG_06 — Ver Estado del Sistema: Domain Model
=========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/logs/uc-log-06/index`.

.. uml::
 :caption: UC_LOG_06 — Domain Model

 @startuml

 left to right direction

 class SystemHealthStatus
 class ETLEjecucion
 class SystemHealthStatus

 SystemHealthStatus --> ETLEjecucion
 ETLEjecucion --> SystemHealthStatus

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/logs/uc-log-06/index`
