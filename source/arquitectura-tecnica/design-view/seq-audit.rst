.. meta::
 :artefacto: AT_DESIGN_MOD_AUDIT
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_audit:

===========================================
Design View — MOD_Audit: Auditoria
===========================================

Patron de interaccion del modulo de auditoria. Muestra la busqueda
de ``AuditEvent`` por tipo y rango de fechas, y la exportacion
asincrona via ``ExportJob``. ``AuditEvent`` es append-only (CNST-025):
ninguna operacion modifica registros existentes.

.. uml::
 :caption: Design View MOD_Audit — busqueda y exportacion de eventos de auditoria.

 @startuml

 actor AGR_AUDITOR

 participant InterfazAuditoria      <<frontend>>
 participant ServicioAuditoria      <<api>>
 participant RepositorioAuditEvent  <<repository>>
 participant ServicioExportacion    <<api>>
 database    AlmacenDatos           <<postgresql>>

 AGR_AUDITOR -> InterfazAuditoria : GET /audit/events\n?event_type=ACCESS_CHANGE\n&from=2026-01-01\n&to=2026-05-01
 activate InterfazAuditoria

 InterfazAuditoria -> ServicioAuditoria : buscarEventos(event_type, rango)
 activate ServicioAuditoria

 ServicioAuditoria -> RepositorioAuditEvent : search(EventType, occurred_at rango)
 activate RepositorioAuditEvent
 RepositorioAuditEvent -> AlmacenDatos : SELECT audit_events\nWHERE event_type=?\nAND occurred_at BETWEEN ? AND ?
 AlmacenDatos --> RepositorioAuditEvent : List<AuditEvent>
 RepositorioAuditEvent --> ServicioAuditoria : resultados
 deactivate RepositorioAuditEvent

 ServicioAuditoria --> InterfazAuditoria : pagina de AuditEvent
 deactivate ServicioAuditoria

 InterfazAuditoria --> AGR_AUDITOR : tabla de eventos
 deactivate InterfazAuditoria

 AGR_AUDITOR -> InterfazAuditoria : POST /audit/export\n{format:PDF, filters}
 activate InterfazAuditoria

 InterfazAuditoria -> ServicioExportacion : exportar(filtros, format:ExportFormat.PDF)
 activate ServicioExportacion

 ServicioExportacion -> AlmacenDatos : INSERT export_jobs{\n  job_id:UUID,\n  format:PDF,\n  state:JobState.QUEUED\n}
 AlmacenDatos --> ServicioExportacion : ExportJob encolado

 ServicioExportacion --> InterfazAuditoria : 202 Accepted {job_id}
 deactivate ServicioExportacion
 InterfazAuditoria --> AGR_AUDITOR : job_id para seguimiento
 deactivate InterfazAuditoria

 note right of AlmacenDatos
   AuditEvent append-only (CNST-025).
   No UPDATE ni DELETE sobre audit_events.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
 :doc:`/arquitectura-tecnica/domain-model/export-job`
