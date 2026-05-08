8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "make_outbound_calls" as make_outbound_calls
 rectangle "MOD_Operator" {
   usecase "UC_OPR_03\nOutbound" as UcOpr03
 }
 make_outbound_calls --> UcOpr03
 @enduml

