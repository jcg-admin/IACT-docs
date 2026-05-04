.. meta::
 :artefacto: AT_UC_AUD_02_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: uc/DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_02_domain:

===================================================
UC_AUD_02 — Buscar Auditoria: Domain Model
===================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/audit/uc-aud-02/index`.

.. uml::
 :caption: UC_AUD_02 — Domain Model

 @startuml

 left to right direction

 class AuditEvent
 class AuditFilter
 class AuditEvent

 AuditEvent --> AuditFilter
 AuditFilter --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/audit/uc-aud-02/index`
