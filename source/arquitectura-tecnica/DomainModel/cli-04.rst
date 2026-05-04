.. meta::
 :artefacto: AT_UC_CLI_04_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_04_domain:

=====================================================
UC_CLI_04 — Solicitar Callback: Domain Model
=====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/caller/uc-cli-04/index`.

.. uml::
 :caption: UC_CLI_04 — Domain Model

 @startuml

 left to right direction

 class CallbackRequest
 class Call
 class IVRSession

 CallbackRequest --> Call
 Call --> IVRSession

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/caller/uc-cli-04/index`
