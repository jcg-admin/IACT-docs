.. _arq-mod-007-diagramas:

================================================
ARQ_MOD_007 — Diagramas de Comportamiento
================================================


Flujo de Emision de Evento de Auditoria
=========================================

.. uml::
 :caption: Secuencia de emision de AuditEvent — post-commit en transaccion separada.

 @startuml

 participant "Servicio de Origen\n(UC_ACC, UC_USR, etc.)" as SVC
 participant "Middleware\nAudit Emitter" as AEM
 database "audit_log\n(PostgreSQL — append-only)" as AREP

 SVC -> SVC : ejecuta operacion de escritura
 SVC -> AEM : notificar evento\n{tipo, usuario, entidad, timestamp}
 note right of SVC
   La operacion principal
   ya fue confirmada en BD.
   El audit no la bloquea.
 end note
 AEM -> AREP : INSERT AuditEvent\n(transaccion separada)

 alt fallo en insercion de audit
   AEM -> AEM : registrar alarma interna\n(no abortar operacion original)
 end

 @enduml

----

Estados del Proceso de Exportacion de Audit
=============================================

.. uml::
 :caption: Estado del job de exportacion de audit log (UC_AUD_03).

 @startuml

 [*] --> Queued : export_audit solicita exportacion
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

 actor "view_general_audit" as VGA
 actor "export_audit" as EA
 actor "generate_compliance_report" as GCR

 component "AuditQueryEndpoint\n(/api/audit/)" as QEP
 component "AuditExportWorker\n(async)" as EW
 component "ComplianceWorker\n(HMAC signer)" as CW
 component "InternalMailbox" as MB

 database "audit_log\n(PostgreSQL — append-only)" as DB

 VGA --> QEP : GET /api/audit/
 EA --> QEP : POST /api/audit/export/
 GCR --> QEP : POST /api/audit/compliance/
 QEP --> DB : SELECT (lectura)
 QEP --> EW : encolar job export
 QEP --> CW : encolar job compliance
 EW --> DB : SELECT rango
 CW --> DB : SELECT periodo
 EW --> MB : archivo CSV/JSON
 CW --> MB : archivo firmado HMAC

 @enduml
