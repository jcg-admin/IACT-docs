.. _uc-log-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "export_logs" as USR
 actor "ExportWorker" as W
 actor "InternalMailbox" as MB
 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExportar Logs" as UC04
   usecase "Seleccionar\nrango y formato" as SEL
   usecase "Notificar\nvia Mailbox" as NOT
 }
 USR --> UC04
 UC04 ..> SEL : <<extend>>
 UC04 ..> W : <<include>>
 W ..> NOT : <<include>>
 NOT --> MB
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
 actor "export_logs" as U
 component "LogExportEndpoint" as EP
 component "ExportWorker\n(async)" as W
 database "LogStore" as LS
 component "InternalMailbox" as MB

 U --> EP : POST /logs/export/
 EP --> W : encolar job
 W --> LS : leer rango
 LS --> W : entries
 W --> MB : entregar archivo
 MB --> U : notificacion
 @enduml

8.4 Secuencia de exportacion de logs
======================================

.. uml::

 @startuml
 actor "export_logs" as U
 participant "LogExportEndpoint" as EP
 participant "ExportWorker" as W
 database "LogStore" as LS
 participant "InternalMailbox" as MB

 U -> EP : POST /logs/export/ {range, format}
 EP -> EP : JWT + RBAC (export_logs)
 alt sin permiso
   EP --> U : 403 Forbidden
 else con permiso
   EP -> EP : validar parametros
   EP -> W : encolar job
   EP --> U : 202 Accepted + job_id
   W -> LS : SELECT logs WHERE range
   LS --> W : entries
   W -> W : formatear CSV/JSON
   W -> MB : INSERT mensaje con adjunto
   MB --> U : notificacion disponible
 end
 @enduml
