.. _uc-log-05-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Consultar logs de infraestructura
================================================================

.. uml::
 :caption: UC_LOG_05 — flujo de consulta de InfraLogStore.

 @startuml

 start
 :Invoker emite GET /api/v1/logs/infra/;
 :Servicio de Aplicacion verifica capability view_infrastructure_logs;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar filtros (host, severity, range);
 :Consultar InfraLogStore;
 :Aplicar filtros;
 :Sanitizar resultados;
 :200 OK con entries de infraestructura;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-pipeline-infraestructura`.
 - :doc:`diagrama-de-secuencia-tail-sse`.
