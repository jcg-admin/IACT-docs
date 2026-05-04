.. _uc-sup-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "broadcast_team_messages" as broadcast_team_messages
 actor "answer_inbound_calls" as answer_inbound_calls
 rectangle "MOD_Supervision" {
   usecase "UC_SUP_03\nBroadcast" as UC
 }
 broadcast_team_messages --> UC
 UC --> answer_inbound_calls
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST broadcast;
 :JWT + RBAC;
 :Validar target;
 :Resolver recipients;
 :Bulk INSERT mailbox;
 if (Urgente?) then (si)
   :SSE push;
 endif
 :Audit BROADCAST_SENT;
 :200;
 stop
 @enduml

8.3 Componentes
===============

.. uml::

 @startuml
 component "Endpoint" as Endpoint
 component "MailboxService" as Mailboxservice
 component "SSE Push" as SsePush
 Endpoint --> Mailboxservice
 Endpoint --> SsePush
 @enduml

8.4 Secuencia urgente
=====================

.. uml::

 @startuml
 actor "broadcast_team_messages" as broadcast_team_messages
 participant "Endpoint" as Endpoint
 queue "MailboxBus" as MailboxBus
 actor "answer_inbound_calls" as answer_inbound_calls
 broadcast_team_messages -> Endpoint: POST broadcast urgente
 Endpoint -> MailboxBus: bulk insert
 MailboxBus -> answer_inbound_calls: SSE push
 answer_inbound_calls -> answer_inbound_calls: toast urgente
 @enduml
