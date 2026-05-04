.. _uc-aud-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "export_audit_log" as export_audit_log
 actor "ExportWorker" as Exportworker
 actor "InternalMailbox" as Internalmailbox
 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Audit Log" as UC03
   usecase "Seleccionar\nperiodo y filtros" as SEL
   usecase "Notificar\nvia Mailbox" as NOT
 }
 export_audit_log --> UC03
 UC03 ..> SEL : <<extend>>
 UC03 ..> Exportworker : <<include>>
 Exportworker ..> NOT : <<include>>
 NOT --> Internalmailbox
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST /audit/export/;
 :JWT + RBAC (export_audit_log);
 :Validar filtros (periodo, accion, user_id);
 if (Filtros invalidos?) then (si)
   :400 Bad Request; stop
 endif
 :Encolar job de exportacion;
 :Emitir audit AUDIT_EXPORT_QUEUED;
 :202 Accepted + job_id;
 fork
   :ExportWorker procesa job;
   :Leer audit_log por filtros;
   :Generar CSV/JSON;
   :Entregar a InternalMailbox;
 endfork
 stop
 @enduml

8.3 Estado del job de exportacion
===================================

.. uml::

 @startuml
 [*] --> Queued
 Queued --> Processing : worker disponible
 Processing --> Done : archivo generado
 Processing --> Failed : error I/O
 Done --> [*] : notificacion enviada
 Failed --> Queued : reintento automatico
 @enduml

8.4 Secuencia de exportacion de audit log
==========================================

.. uml::

 @startuml
 actor "export_audit_log" as export_audit_log
 participant "AuditExportEndpoint" as Auditexportendpoint
 participant "ExportWorker" as Exportworker
 database "Repositorio de Auditoria" as RepositorioDeAuditoria
 participant "InternalMailbox" as Internalmailbox

 export_audit_log -> Auditexportendpoint : POST /audit/export/ {filters}
 Auditexportendpoint -> Auditexportendpoint : JWT + RBAC (export_audit_log)
 alt sin permiso
   Auditexportendpoint --> export_audit_log : 403 Forbidden
 else con permiso
   Auditexportendpoint -> Auditexportendpoint : validar filtros
   Auditexportendpoint -> Exportworker : encolar job
   Auditexportendpoint --> export_audit_log : 202 Accepted + job_id
   Exportworker -> RepositorioDeAuditoria : SELECT FROM audit_log WHERE filters
   RepositorioDeAuditoria --> Exportworker : rows
   Exportworker -> Exportworker : formatear CSV/JSON
   Exportworker -> Internalmailbox : INSERT notificacion con adjunto
   Internalmailbox --> export_audit_log : archivo disponible en buzón
 end
 @enduml
