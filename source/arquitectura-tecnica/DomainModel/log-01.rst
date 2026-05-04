.. meta::
 :artefacto: AT_UC_LOG_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_01_domain:

=============================================================
UC_LOG_01 — Consultar Logs del Sistema: Domain Model
=============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/logs/uc-log-01/index`.

.. uml::
 :caption: UC_LOG_01 — Domain Model

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
 :doc:`/requisitos/casos-uso/logs/uc-log-01/index`
