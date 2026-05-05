8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUD_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "export_audit_log" as INVOKER
 actor "ExportWorker" as WORKER <<sistema>>
 actor "Storage" as STORAGE <<sistema>>
 actor "MailboxService" as MAILBOX <<sistema>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Audit" {
   usecase "UC_AUD_03\nExportar Auditoria\n(async)" as UC_AUD_03
   usecase "Validar formato\n(csv|json)" as VALIDAR_FORMATO
   usecase "Verificar\ninclude_archive (>90d)" as VERIFY_ARCHIVE
   usecase "Encolar export\njob (202)" as ENCOLAR
   usecase "Generar archivo\n(workers)" as GENERAR
   usecase "Persistir en\nStorage" as PERSIST_FILE
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
   usecase "AuditEvent\nAUDIT_EXPORTED (P-39)" as AUDIT
 }

 INVOKER --> UC_AUD_03
 UC_AUD_03 ..> VALIDAR_FORMATO : <<include>>
 UC_AUD_03 ..> VERIFY_ARCHIVE : <<include>>
 UC_AUD_03 ..> ENCOLAR : <<include>>
 ENCOLAR ..> GENERAR : <<include>>
 GENERAR ..> PERSIST_FILE : <<include>>
 GENERAR ..> NOTIFICAR : <<include>>
 GENERAR ..> AUDIT : <<include>>

 ENCOLAR --> WORKER
 PERSIST_FILE --> STORAGE
 NOTIFICAR --> MAILBOX
 Sistema --> AUDIT

 note bottom of UC_AUD_03
   Async — devuelve 202 + job_id.
   Cliente consulta resultado via
   InternalMailbox cuando worker termina.
 end note

 note bottom of NOTIFICAR
   CNST-001 NO email externo.
   CNST-002 mailbox interno.
   CNST-026 sin PII en archivos.
 end note

 note bottom of AUDIT
   P-39 audit reforzado: archivo
   exportado se trata como evento
   sensible. Meta-audit del export
   incluye hash del archivo.
 end note

 @enduml
