.. _uc-aud-02-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Buscar audit (full-text)
======================================================

.. uml::
 :caption: UC_AUD_02 — flujo de busqueda full-text en audit.

 @startuml

 start
 :Invoker emite POST /api/v1/audit/search/;
 :Servicio de Aplicacion verifica capability
   search_audit_log;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar query string + range temporal <= 90d;
 if (Range excedido / query invalido?) then (si)
   :422 query invalido;
   stop
 endif

 :Throttle check (rate limit por user);
 if (Excedido?) then (si)
   :429 Too Many Requests;
   stop
 endif

 :FTS search en indice full-text;
 :Sanitize results (PII filter);
 :Emitir meta-audit AUDIT_SEARCH_QUERIED;
 :200 OK con hits + ranking;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-componentes-fts`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service`.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`.
