8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_own_performance_dashboard" as view_own_performance_dashboard
 rectangle "MOD_Operator" {
   usecase "UC_OPR_08\nMy Dashboard" as UcOpr08
 }
 view_own_performance_dashboard --> UcOpr08
 @enduml

