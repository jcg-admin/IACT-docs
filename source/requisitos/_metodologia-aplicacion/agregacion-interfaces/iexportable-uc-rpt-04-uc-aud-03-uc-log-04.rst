5.1 ``IExportable`` — UC_RPT_04, UC_AUD_03, UC_LOG_04
-----------------------------------------------------

.. uml::

   @startuml
   allowmixing

   interface IExportable <<interface>> {
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   class Reporte {
     - tipo : Enum
     - filtros : Filtro
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   class EventoAuditoria {
     - rango : Rango
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   class LogSistema {
     - rango : Rango
     - servicio : String
     + exportar(formato : Enum) : Archivo
     + estimarFilas() : Integer
     + obtenerSizeMB() : Decimal
   }

   Reporte ..|> IExportable
   EventoAuditoria ..|> IExportable
   LogSistema ..|> IExportable

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
