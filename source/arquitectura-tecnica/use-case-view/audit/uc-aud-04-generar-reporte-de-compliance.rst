.. meta::
 :artefacto: AT_UC_AUD_04_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_aud_04_generar_reporte_de_compliance:

==================================================
UC_AUD_04 — Generar Reporte de Compliance
==================================================

Reporte estandar de compliance para auditorias externas (SOX, ISO):
templates predefinidos (PRIVILEGED_ACCESS, CONFIG_CHANGES,
LOGIN_PATTERNS, SENSITIVE_DATA_ACCESS), formato pdf|csv|json, firmado
HMAC para integridad. Async via ExportWorker. P-39 audit reforzado.

.. uml::
 :caption: UC_AUD_04 — actores y casos asociados.

 @startuml

 left to right direction

 actor "generate_compliance_report" as generate_compliance_report
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "ExportJob" as ExportJob <<sistema>>
 actor "ExportWorker" as ExportWorker <<sistema>>
 actor "AuditQueryService" as AuditQueryService <<sistema>>
 actor "AuditRepo" as AuditRepo <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as UC_AUD_04
   usecase "Verificar\ngenerate_compliance_report" as VERIFICAR_AGR
   usecase "Validar template\n(PRIVILEGED_ACCESS,\nCONFIG_CHANGES, ...)" as VALIDAR_TEMPLATE
   usecase "Validar period\n(date_from..date_to)" as VALIDAR_PERIOD
   usecase "Crear ExportJob\n(202 + job_id)" as CREAR_JOB
   usecase "Consultar AuditRepo\npor template" as QUERY
   usecase "Renderizar reporte\n(pdf|csv|json)" as RENDER
   usecase "Firmar HMAC\n(integridad)" as FIRMAR
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
   usecase "Meta-audit P-39\nCOMPLIANCE_REPORT_GENERATED" as METAAUDIT
 }

 generate_compliance_report --> UC_AUD_04

 UC_AUD_04 ..> VERIFICAR_AGR : <<include>>
 UC_AUD_04 ..> VALIDAR_TEMPLATE : <<include>>
 UC_AUD_04 ..> VALIDAR_PERIOD : <<include>>
 UC_AUD_04 ..> CREAR_JOB : <<include>>
 CREAR_JOB ..> QUERY : <<include>>
 QUERY ..> RENDER : <<include>>
 RENDER ..> FIRMAR : <<include>>
 FIRMAR ..> NOTIFICAR : <<include>>
 FIRMAR ..> METAAUDIT : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 CREAR_JOB --> ExportJob
 CREAR_JOB --> ExportWorker
 QUERY --> AuditQueryService
 AuditQueryService --> AuditRepo
 NOTIFICAR --> InternalMailbox
 METAAUDIT --> AuditService
 AuditService --> view_audit_log

 note bottom of VALIDAR_TEMPLATE
   Templates predefinidos (config/ADR):
   PRIVILEGED_ACCESS, CONFIG_CHANGES,
   LOGIN_PATTERNS, SENSITIVE_DATA_ACCESS.
   No editables.
 end note

 note bottom of FIRMAR
   HMAC sobre contenido + period.
   Garantia de integridad para
   auditorias externas (SOX, ISO).
 end note

 note bottom of METAAUDIT
   P-39 reforzado: incluye hash
   firmado del archivo + template +
   period.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/audit-event` —
   eventos consumidos por templates.
 - :doc:`/arquitectura-tecnica/domain-model/audit-repo` —
   fuente de datos.
 - :doc:`/arquitectura-tecnica/domain-model/audit-query-service` —
   queries por template.
 - :doc:`/arquitectura-tecnica/domain-model/export-job` —
   ExportJob con template + signature.
 - :doc:`/arquitectura-tecnica/domain-model/export-worker` —
   worker async render + sign.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   notifica completacion.
 - :doc:`/arquitectura-tecnica/domain-model/strategy-pattern` —
   ExportFormatStrategy (pdf/csv/json).
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica generate_compliance_report.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   meta-audit P-39.
 - :doc:`/requisitos/casos-uso/audit/uc-aud-04/index` —
   spec textual.
