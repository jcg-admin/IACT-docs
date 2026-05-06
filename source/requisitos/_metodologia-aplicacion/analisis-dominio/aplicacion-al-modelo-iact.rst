Aplicación al modelo IACT
~~~~~~~~~~~~~~~~~~~~~~~~~

Modelo IACT consolidado con multiplicidad anclada a las
reglas del dominio:

.. uml::

   @startuml

   class Call
   class Segment
   class ETLExecution
   class ETLWindow
   class ETLError
   class Report
   class Filter
   class Alert
   class Supervisor
   class User
   class Session
   class Group
   class Function
   class AuditEvent
   class SoDRule

   Call "1..*" -- "1" Segment : belongs to
   ETLWindow "1" -- "0..*" ETLExecution : contains
   ETLExecution "1..*" -- "0..*" Call : loads
   ETLExecution "1" *-- "0..*" ETLError : produces
   Report "1..*" -- "0..*" Call : aggregates
   Report "1" o-- "0..*" Filter : applies
   Alert "0..*" -- "0..1" Supervisor : is acknowledged by
   Session "1" *-- "1" User : belongs to
   User "0..*" o-- "0..*" Group : assigned to
   Group "1..*" o-- "0..*" Function : groups
   User "1" --> "0..*" AuditEvent : generates
   SoDRule "0..*" -- "2..3" Function : restricts
   @enduml
