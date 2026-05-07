.. _uc-pip-04-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Solicitar reintento de ETL
========================================================

.. uml::
 :caption: UC_PIP_04 — flujo de solicitud de reintento.

 @startuml

 start
 :Invoker emite POST /api/v1/etl/reintento/;
 :Servicio de Aplicacion verifica capability request_pipeline_retry;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar trimestre y motivo (min 20 chars);
 if (Parametros invalidos?) then (si)
   :400 Bad Request;
   stop
 endif

 :Verificar que NO hay ETL en ejecucion;
 if (ETL en ejecucion?) then (si)
   :409 Conflict;
   stop
 endif

 :Registrar nueva ejecucion (manual=True);
 :Invocar Disparador ETL (reproceso completo);
 :Emitir audit ETL_REINTENTO_SOLICITADO;
 :202 Accepted con etl_run_id;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`diagrama-de-estados-reintento`.
