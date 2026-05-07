.. _uc-log-07-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar metricas tecnicas
=========================================================

.. uml::
 :caption: UC_LOG_07 — flujo de consulta de metricas.

 @startuml

 start
 :Invoker emite GET /api/v1/metrics/ con period y filtros;
 :Servicio de Aplicacion verifica capability view_technical_metrics;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Cache lookup;
 if (Cache HIT?) then (si)
   :Return cached metrics;
   :200 OK;
   stop
 endif

 :Query TSDB con period y filtros;
 :Compute percentiles (P50, P95, P99);
 :Cache write con TTL;
 :200 OK con metrics + percentiles;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-pipeline-metricas`.
