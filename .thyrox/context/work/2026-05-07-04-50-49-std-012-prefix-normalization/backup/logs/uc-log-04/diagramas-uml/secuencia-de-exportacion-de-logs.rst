8.4 Secuencia de exportacion de logs
======================================

.. uml::

 @startuml
 actor "export_logs" as export_logs
 participant "LogExportEndpoint" as Logexportendpoint
 participant "ExportWorker" as Exportworker
 database "LogStore" as Logstore
 participant "InternalMailbox" as Internalmailbox

 export_logs -> Logexportendpoint : POST /logs/export/ {range, format}
 Logexportendpoint -> Logexportendpoint : JWT + RBAC (export_logs)
 alt sin permiso
   Logexportendpoint --> export_logs : 403 Forbidden
 else con permiso
   Logexportendpoint -> Logexportendpoint : validar parametros
   Logexportendpoint -> Exportworker : encolar job
   Logexportendpoint --> export_logs : 202 Accepted + job_id
   Exportworker -> Logstore : consultar logs por range
   Logstore --> Exportworker : entries
   Exportworker -> Exportworker : formatear CSV/JSON
   Exportworker -> Internalmailbox : registrar mensaje con adjunto
   Internalmailbox --> export_logs : notificacion disponible
 end
 @enduml
