.. _uc-aud-04-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Generar reporte de auditoria firmado
==================================================================

.. uml::
 :caption: UC_AUD_04 — flujo de generacion + firma + entrega.

 @startuml

 start
 :Invoker emite POST /api/v1/audit/reports/ con template + period;
 :Servicio de Aplicacion verifica capability generate_audit_report;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar template existe y period valido;
 if (Parametros invalidos?) then (si)
   :400 Bad Request;
   stop
 endif

 :Crear ReportJob con state=Queued;
 :Encolar en Procesador Asincrono;
 :Audit AUDIT_REPORT_QUEUED;
 :202 Accepted con job_id;

 fork
   :Worker ejecuta template queries contra audit_log;
   :Re-verificar capability del invoker;
   if (Capability revocada?) then (si)
     :Cancelar job + audit AUDIT_REPORT_CANCELLED;
     stop
   endif
   :Sanitize PII;
   :Calcular hash SHA-256;
   :Firmar HMAC con clave KMS;
   :Upload archivo a Storage con URL firmada;
   :Audit AUDIT_REPORT_GENERATED con hash;
   :InternalMailbox notify con URL;
 endfork

 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-flujo-de-firma`.
 - :doc:`diagrama-de-secuencia-verify`.
