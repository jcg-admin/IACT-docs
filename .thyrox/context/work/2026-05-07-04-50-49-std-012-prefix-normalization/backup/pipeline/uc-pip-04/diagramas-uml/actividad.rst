8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST /api/v1/etl/reintento/;
 :JWT + RBAC (request_pipeline_retry);
 :Validar trimestre y motivo (min 20 chars);
 if (ETL en ejecucion?) then (si)
   :409 Conflict; stop
 endif
 :Registrar nueva ejecucion (manual);
 :Invocar Disparador ETL (reproceso completo);
 :Emitir auditoria ETL_REINTENTO_SOLICITADO;
 :202 Accepted con etl_run_id;
 stop
 @enduml

