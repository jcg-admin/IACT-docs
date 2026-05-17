8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 actor "answer_inbound_calls" as answer_inbound_calls
 rectangle "MOD_Caller" {
   usecase "UC_CLI_04\nCallback" as UcCli04
   usecase "UC_OPR_03\nDial" as UcOpr03
 }
 Caller --> UcCli04
 UcCli04 --> answer_inbound_calls
 answer_inbound_calls --> UcOpr03
 UcOpr03 ..> UcCli04 : consume CallbackEntry
 @enduml

