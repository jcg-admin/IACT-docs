.. _uc-log-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "export_logs" as export_logs
 actor "ExportWorker" as Exportworker
 actor "InternalMailbox" as Internalmailbox
 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExportar Logs" as UC04
   usecase "Seleccionar\nrango y formato" as SEL
   usecase "Notificar\nvia Mailbox" as NOT
 }
 export_logs --> UC04
 UC04 ..> SEL : <<extend>>
 UC04 ..> Exportworker : <<include>>
 Exportworker ..> NOT : <<include>>
 NOT --> Internalmailbox
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST /logs/export/;
 :JWT + RBAC (export_logs);
 :Validar rango, formato (CSV/JSON);
 if (Formato invalido?) then (si)
   :400 Bad Request; stop
 endif
 :Encolar job de exportacion;
 :Emitir audit LOG_EXPORT_QUEUED;
 :202 Accepted + job_id;
 fork
   :ExportWorker procesa job;
   :Leer LogStore por rango;
   :Generar archivo exportado;
   :Enviar a InternalMailbox del usuario;
 endfork
 stop
 @enduml

8.3 Componentes export
=======================

.. uml::

 @startuml
 actor "export_logs" as export_logs
 component "LogExportEndpoint" as Logexportendpoint
 component "ExportWorker\n(async)" as Exportworker
 database "LogStore" as Logstore
 component "InternalMailbox" as Internalmailbox

 export_logs --> Logexportendpoint : POST /logs/export/
 Logexportendpoint --> Exportworker : encolar job
 Exportworker --> Logstore : leer rango
 Logstore --> Exportworker : entries
 Exportworker --> Internalmailbox : entregar archivo
 Internalmailbox --> export_logs : notificacion
 @enduml

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
   Exportworker -> Logstore : SELECT logs WHERE range
   Logstore --> Exportworker : entries
   Exportworker -> Exportworker : formatear CSV/JSON
   Exportworker -> Internalmailbox : INSERT mensaje con adjunto
   Internalmailbox --> export_logs : notificacion disponible
 end
 @enduml
