8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "export_logs" as INVOKER
 actor "ExportWorker" as WORKER <<sistema>>
 actor "Storage" as STORAGE <<sistema>>
 actor "MailboxService" as MAILBOX <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_04\nExportar Logs (async)" as UC_LOG_04
   usecase "Validar formato\n(jsonl | csv)" as VALIDAR_FORMATO
   usecase "Verificar\ninclude_archive" as VERIFY_ARCHIVE
   usecase "Encolar export\njob (202)" as ENCOLAR
   usecase "Generar archivo" as GENERAR
   usecase "Persistir en\nStorage" as PERSIST_FILE
   usecase "Notificar via\nInternalMailbox" as NOTIFICAR
 }

 INVOKER --> UC_LOG_04
 UC_LOG_04 ..> VALIDAR_FORMATO : <<include>>
 UC_LOG_04 ..> VERIFY_ARCHIVE : <<include>>
 UC_LOG_04 ..> ENCOLAR : <<include>>
 ENCOLAR ..> GENERAR : <<include>>
 GENERAR ..> PERSIST_FILE : <<include>>
 GENERAR ..> NOTIFICAR : <<include>>

 ENCOLAR --> WORKER
 PERSIST_FILE --> STORAGE
 NOTIFICAR --> MAILBOX

 note bottom of UC_LOG_04
   Async — devuelve 202 + job_id.
   Reusa P-57/P-64/P-65/P-72.
   Patron consistente con UC_AUD_03.
 end note

 note bottom of NOTIFICAR
   CNST-001 NO email externo.
   CNST-002 mailbox interno.
   CNST-026 sin PII.
 end note

 @enduml
