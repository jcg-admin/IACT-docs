8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_system_health" as view_system_health
 rectangle "MOD_Logs" {
   usecase "UC_LOG_06\nEstado Sistema" as UC_LOG_06
   usecase "UC_PIP_01" as UcPip01
   usecase "UC_ALR_02" as UcAlr02
 }
 view_system_health --> UC_LOG_06
 UC_LOG_06 ..> UcPip01 : <<include>>
 UC_LOG_06 ..> UcAlr02 : <<include>>
 @enduml

