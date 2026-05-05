.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_QUERY_SERVICE
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

.. _dm_class_audit_query_service:

=================
AuditQueryService
=================

Servicio de consulta de eventos de auditoria con paginacion y exportacion.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase AuditQueryService — stub pendiente de desarrollo.

 @startuml

 class AuditQueryService {
  + list(filters, cursor, page_size)
  + get(id)
  + aggregate(filters, group_by)
  + export(filters, format)
 }

 @enduml
