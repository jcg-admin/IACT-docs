8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "hold_calls" as hold_calls
 rectangle "MOD_Operator" {
   usecase "UC_OPR_04\nHold/Unhold" as UcOpr04
 }
 hold_calls --> UcOpr04
 @enduml

