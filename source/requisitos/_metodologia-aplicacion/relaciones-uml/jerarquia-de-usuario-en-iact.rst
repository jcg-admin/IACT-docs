6.1 Jerarquía de Usuario en IACT
--------------------------------

.. uml::

   @startuml

   class User {
     - id : Integer
     - email : String
     - password_hash : String
     + login()
     + logout()
   }

   class Operator {
     + viewDashboard()
     + viewActiveAlerts()
   }

   class Supervisor {
     - centers : List<Integer>
     + viewHistoricalReports()
     + acknowledgeAlert()
   }

   class AccessAdmin {
     + assignFunctions()
     + revokeFunctions()
   }

   class PipelineAdmin {
     + superviseETL()
     + requestRetry()
   }

   class Auditor {
     + queryAudit()
     + generateComplianceReport()
   }

   User <|-- Operator
   User <|-- Supervisor
   User <|-- AccessAdmin
   User <|-- PipelineAdmin
   User <|-- Auditor
   note right of User
     Cada rol "es un tipo de"
     User. Todos heredan
     login(), logout().
   end note
   @enduml
