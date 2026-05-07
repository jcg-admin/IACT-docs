.. _uc-aud-03-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Exportar audit log
================================================

.. uml::
 :caption: UC_AUD_03 — flujo asincrono de exportacion.

 @startuml

 start
 :Invoker emite POST /api/v1/audit/export/ con filters;
 :Servicio de Aplicacion verifica capability export_audit_log;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar filtros (periodo, accion, user_id);
 if (Filtros invalidos?) then (si)
   :400 Bad Request;
   stop
 endif

 :Crear ExportJob con state=Queued;
 :Encolar job en el Procesador Asincrono;
 :Emitir audit AUDIT_EXPORT_QUEUED;
 :202 Accepted con job_id;

 fork
   :ExportWorker procesa job asincrono;
   :Cargar audit rows por filtros;
   :Sanitize PII;
   :Generar archivo CSV o JSON;
   :Entregar a InternalMailbox del invoker;
   :Audit AUDIT_EXPORT_DELIVERED;
 endfork

 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`diagrama-de-estados-export-job`.
 - :doc:`/arquitectura-tecnica/domain-model/export-job`.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker`.
