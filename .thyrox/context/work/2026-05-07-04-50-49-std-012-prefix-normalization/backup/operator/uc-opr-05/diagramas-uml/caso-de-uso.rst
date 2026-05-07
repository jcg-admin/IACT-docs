8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "transfer_calls" as transfer_calls
 actor "answer_inbound_calls" as answer_inbound_calls
 rectangle "MOD_Operator" {
   usecase "UC_OPR_05\nTransfer" as UcOpr05
   usecase "Warm" as Warm
   usecase "Cold" as Cold
 }
 transfer_calls --> UcOpr05
 UcOpr05 ..> Warm : <<extend>>
 UcOpr05 ..> Cold : <<extend>>
 Warm --> answer_inbound_calls
 Cold --> answer_inbound_calls
 @enduml

