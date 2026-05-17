3.2 Conversión a clases (vista global del dominio)
--------------------------------------------------

.. uml::

   @startuml

   package "Acceso & RBAC" as MODULO_ACCESO_RBAC {
     class User
     class Session
     class DataSegment
     class Function
     class Group
     class ExceptionalPermission
   }

   package "Llamadas / IVR" as MODULO_LLAMADAS_IVR {
     class Call
     class Center
     class Campaign
     class Service
     class Region
   }

   package "Reportes / Métricas" as MODULO_REPORTES {
     class Report
     class Dashboard
     class Metric
     class Filter
   }

   package "Pipeline ETL" as MODULO_ETL {
     class ETLExecution
     class ETLError
     class LoadedRow
     class Scheduler
   }

   package "Alertas / Notificaciones" as MODULO_ALERTAS {
     class Alert
     class Threshold
     class Subscription
     class InternalMailbox
   }

   package "Auditoría" as MODULO_AUDITORIA {
     class AuditEvent
     class PermissionAudit
     class AccessAudit
   }
   @enduml
