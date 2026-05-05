8.3 Paso 3 — diagrama de contexto integrado
-------------------------------------------

.. uml::

   @startuml
   allowmixing

   skinparam packageStyle rectangle

   package "IACT — sistema completo" {
     package "Catálogo RBAC" {
       class Funcion
       class Grupo
       Grupo "*" o-- "*" Funcion
     }

     package "Pipeline ETL" {
       class EjecucionETL
       class ErrorETL
       EjecucionETL "1" *-- "0..*" ErrorETL
     }

     package "Reportes" {
       interface IExportable <<interface>>
       class Reporte
       class FilaResultado
       Reporte ..|> IExportable
       Reporte "1" *-- "0..*" FilaResultado
     }

     package "Auditoría" {
       class EventoAuditoria
       class DetalleAuditoria
       EventoAuditoria ..|> IExportable
       EventoAuditoria "1" *-- "0..*" DetalleAuditoria
     }

     package "Alertas" {
       interface INotificable <<interface>>
       class Alerta
       class BuzonInterno
       Alerta -- BuzonInterno : usa
       BuzonInterno ..|> INotificable
     }
   }

   note bottom
     ◇ agregación (Grupo–Funcion)
     ● composición (Reporte–FilaResultado,
       EjecucionETL–ErrorETL,
       EventoAuditoria–DetalleAuditoria)
     ..|> realización (IExportable,
                      INotificable)
   end note
   @enduml
