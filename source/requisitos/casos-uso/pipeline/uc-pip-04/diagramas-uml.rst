.. _uc-pip-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "request_pipeline_retry" as request_pipeline_retry
 actor "ETLScheduler" as Etlscheduler
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_04\nReintentar ETL" as UC04
 }
 request_pipeline_retry --> UC04
 UC04 --> Etlscheduler
 @enduml

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

8.3 Estado del reintento
=========================

.. uml::

 @startuml
 [*] --> en_ejecucion : POST reintento aceptado
 en_ejecucion --> exitoso : SP completa sin errores
 en_ejecucion --> fallido : SP lanza error
 exitoso --> [*]
 fallido --> [*] : requiere nuevo reintento
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "request_pipeline_retry" as request_pipeline_retry
 participant "Endpoint" as Endpoint
 database "Registro de\nEjecuciones" as RegistroDe
 participant "Disparador ETL" as DisparadorEtl
 participant "AuditService" as Auditservice
 request_pipeline_retry -> Endpoint: POST /api/v1/etl/reintento/
 Endpoint -> Endpoint: JWT + RBAC + validar
 Endpoint -> RegistroDe: get_activa()
 RegistroDe --> Endpoint: null (sin ejecucion activa)
 Endpoint -> RegistroDe: crear_manual(trimestre, manual)
 RegistroDe --> Endpoint: etl_run_id
 Endpoint -> DisparadorEtl: ejecutar_historico(trimestre)
 Endpoint -> Auditservice: emit ETL_REINTENTO_SOLICITADO
 Endpoint --> request_pipeline_retry: 202 Accepted {etl_run_id}
 @enduml
