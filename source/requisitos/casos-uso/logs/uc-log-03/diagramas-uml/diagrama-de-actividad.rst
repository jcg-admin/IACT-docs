.. _uc-log-03-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Buscar logs (full-text)
=====================================================

.. uml::
 :caption: UC_LOG_03 — flujo de busqueda full-text en logs operacionales.

 @startuml

 start
 :Invoker emite POST /api/v1/logs/search/;
 :Servicio de Aplicacion verifica capability search_logs;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar query string + range temporal;
 :Throttle check (rate limit);
 if (Excedido?) then (si)
   :429 Too Many Requests;
   stop
 endif

 :FTS search en LogStore;
 :Sanitize PII + cap (limit max results);
 :200 OK con hits + ranking;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/requisitos/casos-uso/audit/uc-aud-02/index`
   (UC similar para audit log — comparte arquitectura FTS).
