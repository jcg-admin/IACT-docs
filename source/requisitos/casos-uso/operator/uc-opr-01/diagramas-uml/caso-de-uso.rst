8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "manage_own_agent_state" as manage_own_agent_state
 actor "CallRouter" as Callrouter
 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado" as UC_OPR_01
 }
 manage_own_agent_state --> UC_OPR_01
 UC_OPR_01 --> Callrouter
 @enduml

