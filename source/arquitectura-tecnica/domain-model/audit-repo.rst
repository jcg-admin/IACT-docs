.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_REPO
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

.. _dm_class_audit_repo:

=========
AuditRepo
=========

Repositorio append-only de AuditEvent. No permite actualizar ni eliminar.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase AuditRepo — stub pendiente de desarrollo.

 @startuml

 class AuditRepo {
  + query(filters, cursor, limit)
  + get_by_id(id)
  + aggregate(filters, group_by)
 }

 @enduml
