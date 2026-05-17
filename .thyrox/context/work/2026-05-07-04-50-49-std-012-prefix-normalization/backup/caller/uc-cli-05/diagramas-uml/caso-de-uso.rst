8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 rectangle "MOD_Caller" {
   usecase "UC_CLI_05\nCSAT" as UcCli05
 }
 Caller --> UcCli05
 @enduml

