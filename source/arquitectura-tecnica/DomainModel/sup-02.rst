.. meta::
 :artefacto: AT_UC_SUP_02_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_02_domain:

======================================================
UC_SUP_02 — Barge-in en Llamada: Domain Model
======================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/supervision/uc-sup-02/index`.

.. uml::
 :caption: UC_SUP_02 — Domain Model

 @startuml

 left to right direction

 class Call
 class AgentSession
 class SupervisionChannel

 Call --> AgentSession
 AgentSession --> SupervisionChannel

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-02/index`
