6. Ejemplo completo — clase ``Reporte``
=======================================

.. uml::

   @startuml

   class Report {
     - id : Integer
     - type : Enum
     - name : String
     - filters : Filter
     - applied_segment : DataSegment
     - generated_at : DateTime
     - cache_ttl : Integer
     + generate(filters : Filter) : Report
     + export(format : Enum) : File
     + getResults() : List<Row>
     + getMetadata() : Metadata
     -- responsabilidades --
     Representar un reporte de métricas
     operativas con filtros y segmentación
     aplicados (per BR_012, CNST_008).
   }
   note right of Report
     {type ∈ DASHBOARD | REAL_TIME |
             HISTORICAL | AGENTS |
             QUEUES | CAMPAIGNS}
     {applied_segment != null}
     {cache_ttl ≤ CNST_017 SLA}
   end note
   @enduml
