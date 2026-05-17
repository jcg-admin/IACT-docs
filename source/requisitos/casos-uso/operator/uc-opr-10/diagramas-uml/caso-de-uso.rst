8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "read_own_mailbox" as read_own_mailbox
 actor "read_own_mailbox" as read_own_mailbox
 rectangle "MOD_Operator" {
   usecase "UC_OPR_10\nLeer Mailbox" as UcOpr10
   usecase "UC_SUP_03\nBroadcast" as UcSup03
 }
 read_own_mailbox --> MailboxBus
 UcSup03 ..> UcOpr10 : <<include>>
 read_own_mailbox --> UcOpr10
 @enduml

