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
   Exportworker -> RepositorioDeAuditoria : consultar registros por filtros
   RepositorioDeAuditoria --> Exportworker : rows
   Exportworker -> Exportworker : formatear CSV/JSON
   Exportworker -> Internalmailbox : registrar notificacion con adjunto
   Internalmailbox --> export_audit_log : archivo disponible en buzón
 end
 @enduml
