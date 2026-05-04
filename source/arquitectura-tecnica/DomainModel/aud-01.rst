.. meta::
 :artefacto: AT_UC_AUD_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_01_domain:

==============================================================
UC_AUD_01 — Consultar Auditoria General: Domain Model
==============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/audit/uc-aud-01/index`.

.. uml::
 :caption: UC_AUD_01 — Domain Model

 @startuml

 left to right direction

 class AuditEvent
 class User
 class AuditEvent

 AuditEvent --> User
 User --> AuditEvent

 @enduml


.. uml::
 :caption: UC_AUD_01 — Consultar Auditoria General — Estado de RegistroAuditoria

 @startuml
 hide empty description

 [*] --> Capturado : evento de negocio ocurre
 Capturado --> Indexado : almacenar en BD
 Indexado --> Consultable : indice disponible
 Consultable --> Archivado : politica de retencion
 Archivado --> [*] : purgar segun CNST

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/audit/uc-aud-01/index`
