.. _uc-log-02-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar logs de ETL
====================================================

.. uml::
 :caption: UC_LOG_02 — flujo de consulta de pipeline_runs.

 @startuml

 start
 :Invoker emite GET /api/v1/logs/etl/;
 :Servicio de Aplicacion verifica capability view_pipeline_logs;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar filtros (trimestre, estado);
 :Consultar pipeline_runs en el Almacen de Datos;
 :Filtrar por estado si aplica;
 :Sanitizar resultados;
 :200 OK con lista de ejecuciones ETL;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-componentes-pipeline-log`.
 - :doc:`diagrama-de-secuencia-pipeline-log`.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log`.
 - :doc:`/arquitectura-tecnica/domain-model/log-store`.
