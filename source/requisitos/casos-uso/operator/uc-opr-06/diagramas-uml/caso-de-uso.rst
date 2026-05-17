8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "enter_call_disposition" as enter_call_disposition
 rectangle "MOD_Operator" {
   usecase "UC_OPR_06\nDisposition" as UcOpr06
 }
 enter_call_disposition --> UcOpr06
 @enduml

