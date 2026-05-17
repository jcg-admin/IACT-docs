2.1 Usuario consulta Reporte (UC_RPT)
-------------------------------------

.. uml::

   @startuml

   class User {
     - id : Integer
     - email : String
     + login()
     + queryReport()
   }

   class Report {
     - id : Integer
     - type : Enum
     + generate()
   }

   User "1" --> "0..*" Report : queries

   note right of User
     Asociación:
     un User consulta muchos Reports;
     un Report es consultado por 1 User
     (en una sesión).
   end note
   @enduml
