8.1 Paso 1 — agregación + composición
-------------------------------------

.. uml::

   @startuml
   allowmixing

   class Group
   class Function
   class ETLExecution
   class ETLError

   Group "*" o-- "*" Function           : agregación
   ETLExecution "1" *-- "0..*" ETLError : composición

   note right of Function
     Agregación: Function sobrevive
     al borrado de Group.
   end note
   note right of ETLError
     Composición: ETLError muere
     con la ETLExecution.
   end note
   @enduml
