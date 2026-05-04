8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "manage_own_agent_state" as manage_own_agent_state
 actor "CallRouter" as Callrouter
 rectangle "MOD_Operator" {
   usecase "UC_OPR_01\nCambiar Estado" as UC01
 }
 manage_own_agent_state --> UC01
 UC01 --> Callrouter
 @enduml

