8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "barge_in_calls" as barge_in_calls
 rectangle "MOD_Supervision" {
   usecase "UC_SUP_02\nBarge-in" as UcSup02
   usecase "Take over" as TakeOver
 }
 barge_in_calls --> UcSup02
 UcSup02 ..> TakeOver : <<extend>>
 @enduml

