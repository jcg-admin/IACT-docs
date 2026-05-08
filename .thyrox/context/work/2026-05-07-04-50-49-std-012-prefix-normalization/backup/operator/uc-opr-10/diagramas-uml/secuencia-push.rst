8.4 Secuencia push
==================

.. uml::

 @startuml
 actor "read_own_mailbox" as read_own_mailbox
 participant "Frontend" as Frontend
 queue "MailboxBus" as MailboxBus
 MailboxBus -> Frontend: SSE urgent
 Frontend -> read_own_mailbox: toast
 read_own_mailbox -> Frontend: click read
 Frontend -> MailboxBus: POST read
 @enduml
