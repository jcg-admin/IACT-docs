6.2 Herencia multinivel — Reporte
---------------------------------

.. uml::

   @startuml

   class Report {
     - id : Integer
     - type : Enum
     + generate()
   }

   class OperationalReport {
     - segment : DataSegment
   }

   class RealTimeReport {
     - ttl_sec : Integer
   }

   class HistoricalReport {
     - max_range : Integer
   }

   class AgentsReport
   class QueuesReport
   class CampaignsReport

   Report <|-- OperationalReport
   OperationalReport <|-- RealTimeReport
   OperationalReport <|-- HistoricalReport
   HistoricalReport <|-- AgentsReport
   HistoricalReport <|-- QueuesReport
   HistoricalReport <|-- CampaignsReport
   note right of HistoricalReport
     Multinivel:
       AgentsReport "es un tipo de"
       HistoricalReport que a su vez
       "es un tipo de" OperationalReport
       que es Report.
   end note
   @enduml
