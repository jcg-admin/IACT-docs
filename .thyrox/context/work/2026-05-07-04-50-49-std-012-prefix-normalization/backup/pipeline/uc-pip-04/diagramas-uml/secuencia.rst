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
