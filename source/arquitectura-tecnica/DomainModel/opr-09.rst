.. meta::
 :artefacto: AT_UC_OPR_09_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_09_domain:

===================================================================
UC_OPR_09 — Ver Propio Historial de Llamadas: Domain Model
===================================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-09/index`.

.. uml::
 :caption: UC_OPR_09 — Domain Model

 @startuml

 left to right direction

 class Call
 class AgentSession
 class CallDisposition

 Call --> AgentSession
 AgentSession --> CallDisposition

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-09/index`
