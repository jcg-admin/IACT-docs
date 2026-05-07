.. _uc-log-06-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar estado del sistema
==========================================================

.. uml::
 :caption: UC_LOG_06 — flujo de consulta del Status overall.

 @startuml

 start
 :Invoker emite GET /api/v1/system/status/;
 :Servicio de Aplicacion verifica capability view_system_health;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Cache lookup (TTL corto, ~30s);
 if (Cache HIT?) then (si)
   :Return cached overall status;
   :200 OK;
   stop
 endif

 fork
   :Check services healthcheck;
 fork again
   :Check dependencies healthcheck;
 fork again
   :Query ETL summary (ultima ejecucion);
 fork again
   :Query alerts active count;
 end fork

 :Compute overall status (green/yellow/red);
 :Cache write con TTL;
 :200 OK con system status detallado;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-componentes`.
 - :doc:`diagrama-de-estados-overall`.
 - :doc:`/arquitectura-tecnica/domain-model/system-health`.
 - :doc:`/arquitectura-tecnica/domain-model/technical-metric`.
