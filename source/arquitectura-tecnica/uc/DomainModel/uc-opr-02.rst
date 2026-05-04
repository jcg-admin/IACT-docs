.. meta::
 :artefacto: AT_UC_OPR_02_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_02_domain:

===========================================================
UC_OPR_02 — Atender Llamada Entrante: Domain Model
===========================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-02/index`.

.. uml::
 :caption: UC_OPR_02 — Domain Model

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
 :doc:`/requisitos/casos-uso/operator/uc-opr-02/index`
