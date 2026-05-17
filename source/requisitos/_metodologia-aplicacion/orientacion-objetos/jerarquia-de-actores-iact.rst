3.1 Jerarquía de actores IACT
-----------------------------

.. uml::

   @startuml

   class User {
     - id : Integer
     - email : String
     - password_hash : String
     - is_active : Boolean
     - segment : DataSegment
     - created_at : DateTime
     + login(email, password) : Boolean
     + logout() : void
     + changePassword(old, new) : void
   }

   class Operator {
     + viewDashboard() : Dashboard
     + viewActiveAlerts() : List<Alert>
   }

   class Supervisor {
     - centers : List<Integer>
     + viewHistoricalReports() : List<Report>
     + acknowledgeAlert(id) : void
   }

   class AccessAdmin {
     + assignFunctions(user, functions) : void
     + assignGroup(user, AGR_id) : void
     + grantTemporaryPermission(...) : void
   }

   class PipelineAdmin {
     + superviseETL() : ETLState
     + requestRetry(execution_id) : void
   }

   class Auditor {
     + queryAudit(filters) : List<AuditEvent>
     + generateComplianceReport() : Report
   }

   User <|-- Operator
   User <|-- Supervisor
   User <|-- AccessAdmin
   User <|-- PipelineAdmin
   User <|-- Auditor

   note right of User
     Herencia: cada rol "es un tipo
     de" User. Todos heredan
     login(), logout(),
     changePassword(). El segment
     restringe los datos visibles
     (BR_012).
   end note
   @enduml
