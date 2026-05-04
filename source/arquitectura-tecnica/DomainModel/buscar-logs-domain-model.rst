.. meta::
 :artefacto: AT_UC_LOG_03_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_03_domain_domain_model:

========================
UC_LOG_03 — Domain Model
========================

UC_LOG_03 — Buscar Logs: Domain Model
==============================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/logs/uc-log-03/index`.

.. uml::
 :caption: UC_LOG_03 — Domain Model

 @startuml

 left to right direction

 class LogEntry
 class LogFilter
 class LogEntry

 LogEntry --> LogFilter
 LogFilter --> LogEntry

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/logs/uc-log-03/index`
