Diagrama UML
~~~~~~~~~~~~

.. uml::

   @startuml
   allowmixing

   class University {
     - students : List<Student>
     - name : String
     + addStudent(s : Student)
     + removeStudent(s : Student)
     + transferStudent(s, other)
     + hasStudent(s) : boolean
     + studentCount() : int
   }

   class Student {
     - id : String
     - name : String
     - status : String
     + changeStatus(new : String)
   }

   University o-- "0..*" Student
   note bottom of Student
     Existe independientemente
     de la Universidad
   end note
   @enduml
