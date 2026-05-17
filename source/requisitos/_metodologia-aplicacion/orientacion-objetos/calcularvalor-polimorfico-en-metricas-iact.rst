4.1 ``calcularValor()`` polimórfico en métricas IACT
----------------------------------------------------

.. uml::

   @startuml

   abstract class Metric {
     - name : String
     - segment : DataSegment
     + calculateValue(period : Range) : Decimal
   }

   class AbandonmentRate {
     + calculateValue(period : Range) : Decimal
   }

   class AverageWaitTime {
     + calculateValue(period : Range) : Decimal
   }

   class EfficiencyIndex {
     - answered_weight : Decimal
     - time_weight : Decimal
     + calculateValue(period : Range) : Decimal
   }

   Metric <|-- AbandonmentRate
   Metric <|-- AverageWaitTime
   Metric <|-- EfficiencyIndex

   note right of Metric
     Polimorfismo (BR_016, BR_017, BR_018):
       AbandonmentRate    → abandoned / total × 100
       AverageWaitTime    → SUM(waits) / N
       EfficiencyIndex    → fórmula compuesta
                            ponderada por servicio
   end note
   @enduml
