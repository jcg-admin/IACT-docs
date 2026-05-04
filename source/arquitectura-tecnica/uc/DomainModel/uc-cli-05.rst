.. meta::
 :artefacto: AT_UC_CLI_05_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_05_domain:

===============================================================
UC_CLI_05 — Calificar Atencion Post-Call: Domain Model
===============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/caller/uc-cli-05/index`.

.. uml::
 :caption: UC_CLI_05 — Domain Model

 @startuml

 left to right direction

 class CSATResponse
 class Call
 class CSATResponse

 CSATResponse --> Call
 Call --> CSATResponse

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/caller/uc-cli-05/index`
