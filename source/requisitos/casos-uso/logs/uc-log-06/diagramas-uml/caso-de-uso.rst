8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_system_health" as view_system_health
 rectangle "MOD_Logs" {
   usecase "UC_LOG_06\nEstado Sistema" as UC06
   usecase "UC_PIP_01" as UcPip01
   usecase "UC_ALR_02" as UcAlr02
 }
 view_system_health --> UC06
 UC06 ..> UcPip01 : <<include>>
 UC06 ..> UcAlr02 : <<include>>
 @enduml

