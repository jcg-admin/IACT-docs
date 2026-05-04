8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "acknowledge_alert" as acknowledge_alert
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_03\nReconocer" as UC03
   usecase "Bulk ack" as BulkAck
 }
 acknowledge_alert --> UC03
 acknowledge_alert --> BulkAck
 BulkAck ..> UC03 : <<include>>
 @enduml

