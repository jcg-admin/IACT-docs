.. _uc-pip-02-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Listar ejecuciones fallidas
==========================================================

.. uml::
 :caption: UC_PIP_02 — flujo de consulta de errores.

 @startuml

 start
 :Invoker emite GET /api/v1/etl/errores/ con filtros;
 :Servicio de Aplicacion verifica capability view_pipeline_errors;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar parametros (period, status filter);
 :Consultar PipelineExecutionRepo (state=fallido);
 :200 OK con lista de ejecuciones fallidas + error_message;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`diagrama-de-clases`.
 - :doc:`/arquitectura-tecnica/domain-model/errores-etl-service`.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
