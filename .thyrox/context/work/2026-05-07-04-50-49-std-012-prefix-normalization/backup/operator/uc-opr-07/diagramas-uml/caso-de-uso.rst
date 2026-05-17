8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "request_break" as request_break
 rectangle "MOD_Operator" {
   usecase "UC_OPR_07\nBreak" as UcOpr07
   usecase "UC_OPR_01\nState change" as UcOpr01
 }
 request_break --> UcOpr07
 UcOpr07 ..> UcOpr01 : <<include>>
 @enduml

