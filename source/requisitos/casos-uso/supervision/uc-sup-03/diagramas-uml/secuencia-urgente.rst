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
