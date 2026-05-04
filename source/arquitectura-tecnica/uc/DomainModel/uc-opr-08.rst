.. meta::
 :artefacto: AT_UC_OPR_08_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_08_domain:

=======================================================
UC_OPR_08 — Ver Propio Dashboard: Domain Model
=======================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/operator/uc-opr-08/index`.

.. uml::
 :caption: UC_OPR_08 — Domain Model

 @startuml

 left to right direction

 class AgentDashboard
 class AgentSession
 class Call

 AgentDashboard --> AgentSession
 AgentSession --> Call

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-08/index`
