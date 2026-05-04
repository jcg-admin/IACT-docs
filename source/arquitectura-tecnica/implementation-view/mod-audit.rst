.. meta::
 :artefacto: AT_IMPL_MOD_AUDIT
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_audit:

==========================================
Implementation View — MOD_Audit
==========================================

Componentes y paquetes de codigo del modulo de auditoria.
Cubre consulta de ``AuditEvent`` (append-only, CNST-025) y
exportacion via ``ExportJob`` a PDF/CSV.

.. uml::
 :caption: Implementation View MOD_Audit — componentes de auditoria y exportacion.

 @startuml

 package "MOD_Audit" {
   component "AuditEventView\nExportJobView" as AuditView <<api>>
   component "AuditEventSerializer\nExportJobSerializer" as AuditSerializer <<serializer>>
   component "AuditService\nconsultar AuditEvent\ngenerar ExportJob" as AuditService <<service>>
   component "AuditEventRepository\nExportJobRepository" as AuditRepo <<repository>>
   component "AuditEventORM\nExportJobORM" as AuditORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 AuditView --> AuditSerializer : valida
 AuditView --> AuditService : invoca
 AuditService --> AuditRepo : consulta / persiste
 AuditRepo --> AuditORM : mapea
 AuditORM --> AlmacenDatos : SQL

 note right of AuditService
   AuditEvent append-only <<CNST-025>>: no UPDATE, no DELETE.
   ExportJob{format:PDF|CSV, state:QUEUED→DONE}.
   Filtros: event_type, actor_id, fecha, modulo.
   Solo INSERT en audit_events, nunca UPDATE.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
 :doc:`/arquitectura-tecnica/domain-model/export-job`
