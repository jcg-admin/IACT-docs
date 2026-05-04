.. meta::
 :artefacto: AT_UC_OPR_05_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_05_domain_domain_model:

========================
UC_OPR_05 — Domain Model
========================

UC_OPR_05 — Transferir Llamada: Domain Model
=====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-05/index`.

.. uml::
 :caption: UC_OPR_05 — Domain Model

 @startuml

 left to right direction

 class Call
 class AgentSession
 class Queue

 Call --> AgentSession
 AgentSession --> Queue

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-05/index`
