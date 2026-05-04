.. meta::
 :artefacto: AT_DOMINIO_07_AUDIT
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_audit:

=========================================
Modelo de Dominio — Bounded Context Audit
=========================================

4.7 Audit
---------

Una clase: ``AuditEvent``. Append-only, inmutable (CNST-025). Las
especializaciones historicas ``PermissionAudit`` y ``AccessAudit``
se realizan como valores del enum ``event_type``, no como subclases.

.. uml::
 :caption: Bounded context Audit — registro inmutable de eventos.

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
   + view()                  <<AUD-001>>
   + search()                <<AUD-002>>
   + export()                <<AUD-003>>
   + generate_compliance_report()  <<AUD-004>>
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
   Sin UPDATE, sin DELETE.
   Toda operacion de escritura en el
   dominio emite uno o mas AuditEvent.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
