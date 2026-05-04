8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 rectangle "MOD_Caller" {
   usecase "UC_CLI_02\nNavegar IVR" as UcCli02
   usecase "UC_CLI_03\nEsperar cola" as UcCli03
   usecase "UC_CLI_04\nCallback" as UcCli04
 }
 Caller --> UcCli02
 UcCli02 ..> UcCli03 : <<extend>>
 UcCli02 ..> UcCli04 : <<extend>>
 @enduml

