7. Diagrama de clases integrado del dominio IACT
================================================

Vista global con relaciones (extracto cubriendo los seis
paquetes):

.. uml::

   @startuml

   class User
   class Session
   class DataSegment
   class Function
   class Group
   class Call
   class Report
   class Metric
   class ETLExecution
   class ETLError
   class Alert
   class Threshold
   class InternalMailbox
   class AuditEvent

   ' RBAC
   User "1" -- "0..1" Session             : owns
   User "1" -- "1"   DataSegment          : restricted_by
   User "*" -- "*"   Group                : assigned_to
   Group   "*" -- "*"   Function          : contains

   ' Llamadas → reportes
   Call "0..*" -- "1" DataSegment         : belongs_to
   Report "1"    -- "1..*" Metric         : contains
   Report "*"    -- "0..*" Call           : aggregates

   ' Pipeline
   ETLExecution "1" *-- "0..*" ETLError   : composes
   ETLExecution "0..*" -- "1..*" Call     : loads

   ' Alertas
   Alert "1" -- "1" Threshold             : uses
   Alert "1" -- "0..*" User               : subscribers
   Alert -- InternalMailbox               : notifies_via

   ' Auditoría
   User "1" -- "0..*" AuditEvent          : generates

   note bottom of AuditEvent
     CNST_025 — append-only,
     inmutable, sin delete().
   end note
   note right of InternalMailbox
     CNST_001 — sólo buzón
     interno, NO email.
   end note
   @enduml
