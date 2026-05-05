.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_audit_service:

============
AuditService
============

Servicio de emision de eventos de auditoria. Orquesta validacion, escaneo PII y persistencia.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase AuditService — stub pendiente de desarrollo.

 @startuml

 class AuditService {
  + emit(event)
  + emit_batch(events)
 }

 @enduml
