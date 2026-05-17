8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 actor "CallRouter" as Callrouter
 rectangle "MOD_Caller" {
   usecase "UC_CLI_03\nEsperar cola" as UcCli03
   usecase "UC_CLI_04\nCallback" as UcCli04
 }
 Caller --> UcCli03
 UcCli03 --> Callrouter
 UcCli03 ..> UcCli04 : <<extend>>
 @enduml

