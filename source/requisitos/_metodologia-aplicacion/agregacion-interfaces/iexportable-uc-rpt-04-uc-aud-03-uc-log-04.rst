5.1 ``IExportable`` — UC_RPT_04, UC_AUD_03, UC_LOG_04
-----------------------------------------------------

.. uml::

   @startuml
   allowmixing

   interface IExportable <<interface>> {
     + export(format : Enum) : File
     + estimateRows() : Integer
     + getSizeMB() : Decimal
   }

   class Report {
     - type : Enum
     - filters : Filter
     + export(format : Enum) : File
     + estimateRows() : Integer
     + getSizeMB() : Decimal
   }

   class AuditEvent {
     - range : Range
     + export(format : Enum) : File
     + estimateRows() : Integer
     + getSizeMB() : Decimal
   }

   class SystemLog {
     - range : Range
     - service : String
     + export(format : Enum) : File
     + estimateRows() : Integer
     + getSizeMB() : Decimal
   }

   Report ..|> IExportable
   AuditEvent ..|> IExportable
   SystemLog ..|> IExportable

   note right of IExportable
     Contrato común para tres tipos
     de export en IACT:
       UC_RPT_04 (Reporte)
       UC_AUD_03 (Auditoría)
       UC_LOG_04 (Logs)
     Throttling distinto por formato
     per CNST_019/020.
   end note
   @enduml
