.. meta::
 :artefacto: AT_UC_CLI_04_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_04_domain_estado:

========================================================
UC_CLI_04 — Solicitar Callback — Estado de SesionLlamada
========================================================

.. uml::
 :caption: UC_CLI_04 — Solicitar Callback — Estado de SesionLlamada

 @startuml
 hide empty description

 [*] --> Iniciada : llamada entrante
 Iniciada --> EnIVR : conectar IVR
 EnIVR --> Atendida : agente disponible
 EnIVR --> Abandonada : cliente cuelga
 Atendida --> Completada : finalizar atencion
 Completada --> [*] : registrar CDR
 Abandonada --> [*] : registrar abandono

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/caller/uc-cli-04/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/caller/uc-cli-04/index`
