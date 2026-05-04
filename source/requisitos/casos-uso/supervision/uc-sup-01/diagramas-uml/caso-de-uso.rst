8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "monitor_live_calls" as monitor_live_calls
 actor "answer_inbound_calls" as answer_inbound_calls
 actor "Caller" as Caller
 rectangle "MOD_Supervision" {
   usecase "UC_SUP_01\nMonitor" as UcSup01
 }
 monitor_live_calls --> UcSup01
 UcSup01 --> answer_inbound_calls
 UcSup01 --> Caller
 @enduml

