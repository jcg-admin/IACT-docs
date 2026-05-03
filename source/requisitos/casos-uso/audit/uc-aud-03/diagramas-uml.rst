.. _uc-aud-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "export_audit_log" as USR
 actor "ExportWorker" as EW
 actor "InternalMailbox" as MB
 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Audit Log" as UC03
   usecase "Seleccionar\nperiodo y filtros" as SEL
   usecase "Notificar\nvia Mailbox" as NOT
 }
 USR --> UC03
 UC03 ..> SEL : <<extend>>
 UC03 ..> EW : <<include>>
 EW ..> NOT : <<include>>
 NOT --> MB
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
 actor "export_audit_log" as U
 participant "AuditExportEndpoint" as EP
 participant "ExportWorker" as W
 database "audit_log\n(PostgreSQL)" as DB
 participant "InternalMailbox" as MB

 U -> EP : POST /audit/export/ {filters}
 EP -> EP : JWT + RBAC (export_audit_log)
 alt sin permiso
   EP --> U : 403 Forbidden
 else con permiso
   EP -> EP : validar filtros
   EP -> W : encolar job
   EP --> U : 202 Accepted + job_id
   W -> DB : SELECT FROM audit_log WHERE filters
   DB --> W : rows
   W -> W : formatear CSV/JSON
   W -> MB : INSERT notificacion con adjunto
   MB --> U : archivo disponible en buzón
 end
 @enduml
