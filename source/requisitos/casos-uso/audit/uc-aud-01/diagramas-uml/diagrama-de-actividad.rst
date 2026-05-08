.. _uc-aud-01-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar audit general
=====================================================

.. uml::
 :caption: UC_AUD_01 — flujo de consulta de audit general.

 @startuml

 start
 :Invoker emite GET /api/v1/audit/ con filtros y cursor;
 :Servicio de Aplicacion verifica capability view_audit_log;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar parametros (filters, page_size, cursor);
 if (Parametros invalidos?) then (si)
   :400 Bad Request;
   stop
 endif

 :Query AuditRepo aplicando cursor + filters;
 :Sanitize rows (PII filter, redact patterns);
 :Build cursor para next page;
 :Emitir meta-audit GENERAL_AUDIT_QUERIED;
 if (Meta-audit ok?) then (no)
   :503 Service Unavailable;
   stop
 endif

 :200 OK con rows + cursor;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-event`.
 - :doc:`/arquitectura-tecnica/domain-model/cursor-encoder`.
