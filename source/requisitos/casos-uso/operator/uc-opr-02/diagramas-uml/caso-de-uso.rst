8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "answer_inbound_calls" as answer_inbound_calls
 actor "CallRouter" as Callrouter
 rectangle "MOD_Operator" {
   usecase "UC_OPR_02\nAnswer" as UcOpr02
 }
 answer_inbound_calls --> UcOpr02
 Callrouter --> UcOpr02
 @enduml

