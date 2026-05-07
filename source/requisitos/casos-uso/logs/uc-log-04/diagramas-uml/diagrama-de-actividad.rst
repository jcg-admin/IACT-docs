.. _uc-log-04-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Exportar logs
============================================

.. uml::
 :caption: UC_LOG_04 — flujo asincrono de exportacion.

 @startuml

 start
 :Invoker emite POST /api/v1/logs/export/;
 :Servicio de Aplicacion verifica capability export_logs;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar rango y formato (CSV o JSON);
 if (Formato invalido?) then (si)
   :400 Bad Request;
   stop
 endif

 :Encolar ExportJob;
 :Emitir audit LOG_EXPORT_QUEUED;
 :202 Accepted con job_id;

 fork
   :ExportWorker procesa job;
   :Leer LogStore por rango;
   :Generar archivo exportado;
   :Sanitize PII;
   :Entregar a InternalMailbox del invoker;
 endfork

 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-componentes-export`.
 - :doc:`diagrama-de-secuencia-exportacion-logs`.
