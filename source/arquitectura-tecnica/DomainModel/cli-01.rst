.. meta::
 :artefacto: AT_UC_CLI_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_01_domain:

=================================================================
UC_CLI_01 — Iniciar Llamada al Call Center: Domain Model
=================================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/caller/uc-cli-01/index`.

.. uml::
 :caption: UC_CLI_01 — Domain Model

 @startuml

 left to right direction

 class Call
 class PBX
 class IVRSession

 Call --> PBX
 PBX --> IVRSession

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/caller/uc-cli-01/index`
