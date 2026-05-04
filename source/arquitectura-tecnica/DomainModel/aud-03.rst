.. meta::
 :artefacto: AT_UC_AUD_03_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_03_domain:

=====================================================
UC_AUD_03 — Exportar Auditoria: Domain Model
=====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/audit/uc-aud-03/index`.

.. uml::
 :caption: UC_AUD_03 — Domain Model

 @startuml

 left to right direction

 class AuditEvent
 class ArchivoExportado
 class AuditEvent

 AuditEvent --> ArchivoExportado
 ArchivoExportado --> AuditEvent

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/audit/uc-aud-03/index`
