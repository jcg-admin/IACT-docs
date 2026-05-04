.. _arq-mod-007-diagramas:

================================================
ARQ_MOD_007 — Diagramas de Comportamiento
================================================


Flujo de Emision de Evento de Auditoria
=========================================

.. uml::
 :caption: Secuencia de emision de AuditEvent — post-commit en transaccion separada.

 @startuml

 participant "Servicio de Origen\n(UC_ACC, UC_USR, etc.)" as ServicioDeOrigen
 participant "Middleware\nAudit Emitter" as Middleware
 database "audit_log\n(PostgreSQL — append-only)" as AREP

 ServicioDeOrigen -> ServicioDeOrigen : ejecuta operacion de escritura
 ServicioDeOrigen -> Middleware : notificar evento\n{tipo, usuario, entidad, timestamp}
 note right of ServicioDeOrigen
   La operacion principal
   ya fue confirmada en BD.
   El audit no la bloquea.
 end note
 Middleware -> AREP : INSERT AuditEvent\n(transaccion separada)

 alt fallo en insercion de audit
   Middleware -> Middleware : registrar alarma interna\n(no abortar operacion original)
 end

 @enduml

----

Estados del Proceso de Exportacion de Audit
=============================================

.. uml::
 :caption: Estado del job de exportacion de audit log (UC_AUD_03).

 @startuml

 [*] --> Queued : export_audit_log solicita exportacion
 Queued --> Processing : ExportWorker disponible
 Processing --> Done : archivo generado y firmado HMAC
 Processing --> Failed : error I/O o timeout
 Done --> [*] : notificacion enviada via InternalMailbox
 Failed --> Queued : reintento automatico

 note right of Done
   El archivo lleva firma HMAC
   para verificacion de
   integridad (generate_compliance_report).
 end note

 @enduml

----

Diagrama de componentes — MOD_Audit
=======================================

.. uml::
 :caption: Componentes de MOD_Audit y sus dependencias.

 @startuml

 actor "view_audit_log" as view_audit_log
 actor "export_audit_log" as export_audit_log
 actor "generate_compliance_report" as generate_compliance_report

 component "AuditQueryEndpoint\n(/api/audit/)" as Auditqueryendpoint
 component "AuditExportWorker\n(async)" as Auditexportworker
 component "ComplianceWorker\n(HMAC signer)" as Complianceworker
 component "InternalMailbox" as Internalmailbox

 database "audit_log\n(PostgreSQL — append-only)" as audit_log

 view_audit_log --> Auditqueryendpoint : GET /api/audit/
 export_audit_log --> Auditqueryendpoint : POST /api/audit/export/
 generate_compliance_report --> Auditqueryendpoint : POST /api/audit/compliance/
 Auditqueryendpoint --> audit_log : SELECT (lectura)
 Auditqueryendpoint --> Auditexportworker : encolar job export
 Auditqueryendpoint --> Complianceworker : encolar job compliance
 Auditexportworker --> audit_log : SELECT rango
 Complianceworker --> audit_log : SELECT periodo
 Auditexportworker --> Internalmailbox : archivo CSV/JSON
 Complianceworker --> Internalmailbox : archivo firmado HMAC

 @enduml
