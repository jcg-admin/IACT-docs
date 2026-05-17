8.3 Paso 3 — diagrama de contexto integrado
-------------------------------------------

.. uml::

   @startuml
   allowmixing

   skinparam packageStyle rectangle

   package "IACT — sistema completo" {
     package "Catálogo RBAC" {
       class Function
       class Group
       Group "*" o-- "*" Function
     }

     package "Pipeline ETL" {
       class ETLExecution
       class ETLError
       ETLExecution "1" *-- "0..*" ETLError
     }

     package "Reportes" {
       interface IExportable <<interface>>
       class Report
       class ResultRow
       Report ..|> IExportable
       Report "1" *-- "0..*" ResultRow
     }

     package "Auditoría" {
       class AuditEvent
       class AuditDetail
       AuditEvent ..|> IExportable
       AuditEvent "1" *-- "0..*" AuditDetail
     }

     package "Alertas" {
       interface INotifiable <<interface>>
       class Alert
       class InternalMailbox
       Alert -- InternalMailbox : uses
       InternalMailbox ..|> INotifiable
     }
   }

   note bottom
     ◇ agregación (Group–Function)
     ● composición (Report–ResultRow,
       ETLExecution–ETLError,
       AuditEvent–AuditDetail)
     ..|> realización (IExportable,
                      INotifiable)
   end note
   @enduml
