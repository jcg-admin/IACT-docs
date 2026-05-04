.. meta::
 :artefacto: AT_DM_CLASS_AUDIT_EVENT
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_audit_event:

==========
AuditEvent
==========

Registro inmutable de un evento en el sistema. Append-only por
CNST-025: sin actualizaciones, sin eliminaciones. Las
especializaciones ``PermissionAudit`` y ``AccessAudit`` se
representan como valores del enum ``EventType``, no como subclases.

.. uml::
 :caption: Clase AuditEvent — registro de auditoria append-only.

 @startuml

 class AuditEvent {
   + event_id : UUID                 <<inmutable>>
   + actor_user_id : UUID
   + event_type : EventType
   + target_entity_type : String
   + target_entity_id : String
   + occurred_at : DateTime
   + details : JSON
   --
   + record()                <<sistema; inmutable per CNST-025>>
   + view()                  <<view_audit_log>>
   + search()                <<search_audit_log>>
   + export()                <<export_audit_log>>
   + generate_compliance_report()  <<generate_compliance_report>>
 }

 enum EventType {
   LOGIN
   LOGOUT
   ACCESS_CHANGE
   PERMISSION_GRANT
   PERMISSION_REVOKE
   EXPORT_REQUESTED
   ALERT_ACKNOWLEDGED
   ETL_RETRY
   SCHEDULE_MODIFIED
   CONFIG_CHANGED
 }

 AuditEvent -- EventType

 note right of AuditEvent
   CNST-025: append-only, inmutable.
   Sin actualizar, sin eliminar.
   Toda operacion de escritura emite AuditEvent.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-audit`
