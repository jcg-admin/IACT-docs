.. meta::
 :artefacto: AT_UC_OPR_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_01_domain:

============================================================
UC_OPR_01 — Cambiar Estado del Agente: Domain Model
============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-01/index`.

.. uml::
 :caption: UC_OPR_01 — Domain Model

 @startuml

 left to right direction

 class AgentSession
 class AgentState
 class AuditEvent

 AgentSession --> AgentState
 AgentState --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-01/index`
