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

