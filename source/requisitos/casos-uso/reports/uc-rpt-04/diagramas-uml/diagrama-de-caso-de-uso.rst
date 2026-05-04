8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_04 — export

 @startuml
 left to right direction
 actor "export_csv" as export_csv
 actor "ExportWorker" as Exportworker
 actor "MailboxService" as Mailboxservice

 rectangle "MOD_Reports" {
   usecase "UC_RPT_04\nExport" as UC04
   usecase "Encolar Job" as EncolarJob
   usecase "Audit eventos" as AuditEventos
   usecase "Notify mailbox" as NotifyMailbox
 }

 export_csv --> UC04
 UC04 ..> EncolarJob : <<include>>
 UC04 ..> AuditEventos : <<include>>
 Exportworker ..> AuditEventos : <<include>>
 Exportworker ..> NotifyMailbox : <<include>>
 NotifyMailbox --> Mailboxservice

 note bottom
   Async via worker. URL firmado
   TTL 24h. CNST-002 mailbox.
 end note

 @enduml

