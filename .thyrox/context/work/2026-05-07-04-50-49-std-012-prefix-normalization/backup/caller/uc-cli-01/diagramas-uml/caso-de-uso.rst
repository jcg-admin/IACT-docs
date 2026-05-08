8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 actor "Telephony" as Telephony
 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nIniciar llamada" as UcCli01
   usecase "UC_CLI_02\nNavegar IVR" as SistemaIVR
 }
 Caller --> UcCli01
 UcCli01 --> Telephony
 UcCli01 ..> IVR : <<include>>
 @enduml

