8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "broadcast_team_messages" as broadcast_team_messages
 actor "answer_inbound_calls" as answer_inbound_calls
 rectangle "MOD_Supervision" {
   usecase "UC_SUP_03\nBroadcast" as UcSup03
 }
 broadcast_team_messages --> UcSup03
 UcSup03 --> answer_inbound_calls
 @enduml

