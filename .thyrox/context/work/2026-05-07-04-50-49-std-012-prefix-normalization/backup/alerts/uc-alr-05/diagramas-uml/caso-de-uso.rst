8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User" as User
 actor "subscribe_to_alert" as subscribe_to_alert
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_05\nSubscriptions" as UC_ALR_05
   usecase "Bulk add" as BulkAdd
   usecase "Mute global" as MuteGlobal
 }
 User --> UC_ALR_05
 subscribe_to_alert --> UC_ALR_05
 UC_ALR_05 ..> BulkAdd : <<extend>>
 User --> MuteGlobal
 @enduml

