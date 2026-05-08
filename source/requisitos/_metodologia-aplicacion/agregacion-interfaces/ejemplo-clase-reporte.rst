6.1 Ejemplo — clase ``Reporte``
-------------------------------

.. uml::

   @startuml
   allowmixing

   class Report {
     - applied_segment : DataSegment
     - cache_ttl : Integer
     - raw_sql : String
     # recordQuery()
     # invalidateCache()
     + generate(filters : Filter)
     + export(format : Enum)
     + getResults()
   }
   note right of Report
     Visibilidad:
       + generate / export / getResults
         → interfaz pública del UC_RPT
       # recordQuery / invalidateCache
         → heredable por subtipos
         (HistoricalReport, AgentsReport...)
       - applied_segment / cache_ttl /
         raw_sql → detalles internos
         (segmentación BR_012, SLA CNST_017)
   end note
   @enduml
