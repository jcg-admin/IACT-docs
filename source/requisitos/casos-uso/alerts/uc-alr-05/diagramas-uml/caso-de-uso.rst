8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "User" as User
 actor "subscribe_to_alert" as subscribe_to_alert
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_05\nSubscriptions" as UC05
   usecase "Bulk add" as BulkAdd
   usecase "Mute global" as MuteGlobal
 }
 User --> UC05
 subscribe_to_alert --> UC05
 UC05 ..> BulkAdd : <<extend>>
 User --> MuteGlobal
 @enduml

