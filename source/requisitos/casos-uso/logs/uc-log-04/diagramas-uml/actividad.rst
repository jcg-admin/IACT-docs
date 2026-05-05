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

