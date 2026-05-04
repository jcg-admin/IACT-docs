.. meta::
 :artefacto: AT_UC_SUP_03_DOMAIN_DOMAIN_MODEL
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_domain_domain_model:

========================
UC_SUP_03 — Domain Model
========================

UC_SUP_03 — Mensaje Broadcast al Equipo: Domain Model
==============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index`.

.. uml::
 :caption: UC_SUP_03 — Domain Model

 @startuml

 left to right direction

 class InternalMailbox
 class AgentSession
 class Team

 InternalMailbox --> AgentSession
 AgentSession --> Team

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index`
