8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "share_report" as share_report
 actor "Receptor User" as ReceptorUser
 actor "MailboxService" as Mailboxservice

 rectangle "MOD_Reports" {
   usecase "UC_RPT_11\nCompartir" as UC11
   usecase "Aplicar share" as AplicacionFrontend
   usecase "Mailbox notify" as MailboxNotify
 }

 share_report --> UC11
 UC11 ..> MailboxNotify : <<include>>
 MailboxNotify --> Mailboxservice
 ReceptorUser --> APP
 APP ..> UC11 : <<extend>>
 @enduml

