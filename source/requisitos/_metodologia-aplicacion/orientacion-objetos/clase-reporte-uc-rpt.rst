5.1 Clase ``Reporte`` (UC_RPT)
------------------------------

.. uml::

   @startuml

   class Report {
     == interfaz pública ==
     + generate(filters : ReportFilter) : Report
     + export(format : Enum) : File
     + getResults() : List<Row>
     + getMetadata() : Metadata
     == privado / oculto ==
     - validateUserSegment()
     - buildSQLQuery()
     - applySegmentFilters()
     - cacheResult()
     - recordQuery()
     - applyThrottling(format)
   }
   note right of Report
     El cliente sólo ve:
       generate(), export(),
       getResults(),
       getMetadata()
     El sistema gestiona internamente:
       segmentación (CNST_008), SQL,
       cache, auditoría, throttling
       (CNST_020).
   end note
   @enduml
