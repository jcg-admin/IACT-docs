3.2 Multiplicidades canónicas IACT
----------------------------------

.. uml::

   @startuml

   class User
   class Session
   class DataSegment
   class Group
   class Function
   class Call
   class Report
   class ETLExecution
   class ETLError
   class Alert
   class Subscription

   User "1" -- "0..1" Session             : owns
   User "1" -- "1"   DataSegment          : restricted
   User "*" -- "*"   Group                : assigned
   Group   "*" -- "*"   Function          : contains
   Report "1" -- "0..*" Call              : aggregates
   ETLExecution "1" -- "0..*" ETLError    : compose
   ETLExecution "1" -- "1..*" Call        : loads
   Alert "1" -- "0..*" Subscription       : has
   Subscription "0..*" -- "1" User        : belongs

   note right of User
     - User:Session = 1:0..1 (CNST_002 sesión única)
     - User:DataSegment = 1:1 (BR_012)
     - Report:Call = 1:0..* (filtro CNST_008)
     - ETLExecution:Call = 1:1..*
     - Alert:Subscriber = 1:0..*
   end note
   @enduml
