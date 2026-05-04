.. meta::
 :artefacto: AT_UC_CLI_02_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_02_domain:

==============================================
UC_CLI_02 — Navegar IVR: Domain Model
==============================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/caller/uc-cli-02/index`.

.. uml::
 :caption: UC_CLI_02 — Domain Model

 @startuml

 left to right direction

 class IVRSession
 class IVRMenu
 class Call

 IVRSession --> IVRMenu
 IVRMenu --> Call

 @enduml


.. uml::
 :caption: UC_CLI_02 — Navegar IVR — Estado de SesionLlamada

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
 :doc:`/requisitos/casos-uso/caller/uc-cli-02/index`
