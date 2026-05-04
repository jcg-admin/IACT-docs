.. _uc-opr-10-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

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

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /me/mailbox;
 :JWT;
 :Query mailbox;
 :Filter status;
 :200;
 stop
 @enduml

8.3 Estado mensaje
==================

.. uml::

 @startuml
 [*] --> sent
 sent --> delivered
 delivered --> read : POST read
 read --> archived
 archived --> [*]
 @enduml

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
