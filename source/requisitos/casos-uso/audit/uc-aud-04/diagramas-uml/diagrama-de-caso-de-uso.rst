8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUD_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "generate_compliance_report" as INVOKER
 actor "ExportWorker" as WORKER <<sistema>>
 actor "ExportJob" as JOB <<sistema>>
 actor "AuditQueryService" as AQS <<sistema>>
 actor "AuditRepo" as AR <<sistema>>
 actor "InternalMailbox" as MB <<sistema>>
 actor "AuditService" as AS <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as UC_AUD_04
   usecase "Validar template\n(PRIVILEGED_ACCESS,\nCONFIG_CHANGES, ...)" as VALIDAR_TEMPLATE
   usecase "Validar period\n(date_from..date_to)" as VALIDAR_PERIOD
   usecase "Crear ExportJob\n(202 + job_id)" as CREATE_JOB
   usecase "Consultar AuditRepo\npor template" as QUERY
   usecase "Renderizar reporte\n(pdf|csv|json)" as RENDER
   usecase "Firmar HMAC\n(integridad)" as FIRMAR
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
   usecase "Emitir meta-audit\nP-39 reforzado" as METAAUDIT
 }

 INVOKER --> UC_AUD_04
 UC_AUD_04 ..> VALIDAR_TEMPLATE : <<include>>
 UC_AUD_04 ..> VALIDAR_PERIOD : <<include>>
 UC_AUD_04 ..> CREATE_JOB : <<include>>
 CREATE_JOB ..> QUERY : <<include>>
 QUERY ..> RENDER : <<include>>
 RENDER ..> FIRMAR : <<include>>
 FIRMAR ..> NOTIFICAR : <<include>>
 FIRMAR ..> METAAUDIT : <<include>>

 CREATE_JOB --> JOB
 CREATE_JOB --> WORKER
 QUERY --> AQS
 AQS --> AR
 NOTIFICAR --> MB
 METAAUDIT --> AS

 note bottom of VALIDAR_TEMPLATE
   Templates: PRIVILEGED_ACCESS,
   CONFIG_CHANGES, LOGIN_PATTERNS,
   SENSITIVE_DATA_ACCESS.
   No editables (config/ADR).
 end note

 note bottom of FIRMAR
   HMAC sobre contenido + period.
   Garantiza integridad para
   auditorías externas (SOX, ISO).
 end note

 note bottom of METAAUDIT
   P-39 audit reforzado:
   COMPLIANCE_REPORT_GENERATED
   con hash del archivo + template
   + period.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   eventos consumidos por templates de compliance.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   fuente de datos para los templates.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   servicio que ejecuta queries por template.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   entidad ExportJob con campo template + signature.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker` —
   worker que renderiza pdf|csv|json.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon donde se notifica completacion del reporte.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor del meta-audit COMPLIANCE_REPORT_GENERATED (P-39).
