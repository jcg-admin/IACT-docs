.. _uc-log-01-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar logs de sistema
========================================================

.. uml::
 :caption: UC_LOG_01 — flujo de consulta de logs.

 @startuml

 start
 :Invoker emite GET /api/v1/logs/system/;
 :Servicio de Aplicacion verifica capability view_application_logs;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar parametros (range, level, source);
 if (Range excedido o invalido?) then (si)
   :422 Unprocessable Entity;
   stop
 endif

 :Query LogStore con filtros;
 :Sanitize PII;
 :200 OK con entries paginadas;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-pipeline`.
 - :doc:`diagrama-de-tail-sse`.
 - :doc:`/arquitectura-tecnica/domain-model/log-store`.
 - :doc:`/arquitectura-tecnica/domain-model/application-log`.
 - :doc:`/arquitectura-tecnica/domain-model/pii-scanner`.
