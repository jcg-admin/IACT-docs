8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_own_call_history" as view_own_call_history
 rectangle "MOD_Operator" {
   usecase "UC_OPR_09\nMy History" as UcOpr09
 }
 view_own_call_history --> UcOpr09
 @enduml

