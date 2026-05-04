.. meta::
 :artefacto: AT_UC_OPR_10_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_10_domain:

==================================================================
UC_OPR_10 — Recibir Notificacion Supervisor: Domain Model
==================================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-10/index`.

.. uml::
 :caption: UC_OPR_10 — Domain Model

 @startuml

 left to right direction

 class InternalMailbox
 class AgentSession
 class InternalMailbox

 InternalMailbox --> AgentSession
 AgentSession --> InternalMailbox

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-10/index`
