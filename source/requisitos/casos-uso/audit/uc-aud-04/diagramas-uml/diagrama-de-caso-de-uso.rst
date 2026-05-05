8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUD_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "generate_compliance_report" as INVOKER
 actor "ComplianceWorker" as WORKER <<sistema>>
 actor "AuditRepo" as REPO <<sistema>>
 actor "HMACSigner" as SIGNER <<sistema>>
 actor "MailboxService" as MAILBOX <<sistema>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_04\nGenerar Reporte\nCompliance" as UC_AUD_04
   usecase "Validar template\n(PRIVILEGED_ACCESS,\nCONFIG_CHANGES, ...)" as VALIDAR_TEMPLATE
   usecase "Validar period\n(date_from..date_to)" as VALIDAR_PERIOD
   usecase "Encolar job\n(202)" as ENCOLAR
   usecase "Consultar AuditRepo\npor template" as QUERY
   usecase "Renderizar reporte\n(pdf|csv|json)" as RENDER
   usecase "Firmar digitalmente\n(HMAC)" as FIRMAR
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
   usecase "Meta-audit\nP-39 reforzado" as METAAUDIT
 }

 INVOKER --> UC_AUD_04
 UC_AUD_04 ..> VALIDAR_TEMPLATE : <<include>>
 UC_AUD_04 ..> VALIDAR_PERIOD : <<include>>
 UC_AUD_04 ..> ENCOLAR : <<include>>
 ENCOLAR ..> QUERY : <<include>>
 QUERY ..> RENDER : <<include>>
 RENDER ..> FIRMAR : <<include>>
 FIRMAR ..> NOTIFICAR : <<include>>
 FIRMAR ..> METAAUDIT : <<include>>

 ENCOLAR --> WORKER
 QUERY --> REPO
 FIRMAR --> SIGNER
 NOTIFICAR --> MAILBOX
 Sistema --> METAAUDIT

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
