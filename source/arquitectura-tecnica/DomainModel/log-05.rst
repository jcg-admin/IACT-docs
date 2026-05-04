.. meta::
 :artefacto: AT_UC_LOG_05_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_05_domain:

==============================================================
UC_LOG_05 — Ver Logs de Infraestructura: Domain Model
==============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/logs/uc-log-05/index`.

.. uml::
 :caption: UC_LOG_05 — Domain Model

 @startuml

 left to right direction

 class InfraLogEntry
 class Nodo
 class InfraLogEntry

 InfraLogEntry --> Nodo
 Nodo --> InfraLogEntry

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/logs/uc-log-05/index`
