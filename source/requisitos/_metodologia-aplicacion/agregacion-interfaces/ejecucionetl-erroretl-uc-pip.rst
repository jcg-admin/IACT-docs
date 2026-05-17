3.1 EjecucionETL ● ErrorETL (UC_PIP)
------------------------------------

.. uml::

   @startuml
   allowmixing

   class ETLExecution {
     - id : Integer
     - start_date : DateTime
     - end_date : DateTime
     - state : Enum
     + loadFromIVR()
   }

   class ETLError {
     - code : String
     - message : String
     - table : String
     - timestamp : DateTime
   }

   class LoadedRow {
     - table : String
     - source_id : Integer
     - timestamp : DateTime
   }

   ETLExecution "1" *-- "0..*" ETLError    : composes
   ETLExecution "1" *-- "0..*" LoadedRow   : composes

   note right of ETLExecution
     Composición:
       si la ETLExecution se purga
       (UC_PIP), sus ETLError y
       LoadedRow se eliminan
       en cascada. No tienen
       sentido fuera de la
       ejecución que los generó.
   end note
   @enduml
