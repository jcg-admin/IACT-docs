7.1 Asociaciones canónicas IACT
-------------------------------

.. uml::

   @startuml

   class User
   class Session
   class Group
   class Function
   class DataSegment
   class Report
   class Alert

   User "1" -- "0..1" Session            : owns
   User "1" -- "1"   DataSegment         : restricted_by
   User "*" -- "*"   Group               : assigned_to
   Group   "*" -- "*"   Function         : contains
   User "1" -- "0..*" Report             : queries
   User "1" -- "0..*" Alert              : subscribed_to

   note right of User
     - User posee 0..1 Session            (CNST_002)
     - User tiene 1 segment               (BR_012)
     - User en 0..* groups                (UC_PERM_01)
     - Group contiene 0..* functions      (UC_PERM_06)
     - User consulta 0..* reports         (UC_RPT)
     - User suscrito a 0..* alerts        (UC_ALR_05)
   end note
   @enduml
