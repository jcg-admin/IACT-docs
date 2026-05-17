9.2 Asignacion entre Usuario y Funcion (UC_ACC_01)
--------------------------------------------------

.. uml::

   @startuml

   class User
   class Function

   class Assignment {
     - start_date : DateTime
     - end_date : DateTime
     - approver : User
     - is_temporary : Boolean
     - justification : String
     + revoke()
     + extend(new_date)
   }

   User "0..*" -- "0..*" Function : assigned
   (User, Function) .. Assignment
   note right of Assignment
     Cuando is_temporary = true,
     CNST_031 obliga
     end_date ≤ start_date + 6
     meses y justification con
     ≥ 20 caracteres.
   end note
   @enduml
