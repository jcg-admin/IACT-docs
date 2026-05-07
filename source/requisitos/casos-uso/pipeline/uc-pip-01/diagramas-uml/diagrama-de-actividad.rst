.. _uc-pip-01-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Supervisar ejecucion ETL
======================================================

.. uml::
 :caption: UC_PIP_01 — flujo de supervision general del ETL.

 @startuml

 start
 :Invoker emite GET /api/v1/etl/supervision/;
 :Servicio de Aplicacion verifica capability view_pipeline_status;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Consultar Registro de Ejecuciones (PipelineExecutionRepo);
 :Construir ResumenSalud (estado general + ultima ejecucion);
 :200 OK con estado general;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
 - :doc:`diagrama-de-estados-ejecucion-etl`.
 - :doc:`/arquitectura-tecnica/domain-model/supervision-etl-service`.
 - :doc:`/arquitectura-tecnica/domain-model/resumen-salud`.
 - :doc:`/arquitectura-tecnica/domain-model/resumen-salud-builder`.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`.
