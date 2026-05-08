8.3 Clases
==========

.. uml::

 @startuml
 class AlertHistoryService
 class AlertRepo {
   query_history(filters, period)
 }
 class TimingCalculator {
   compute_ttak, compute_ttar
 }
 AlertHistoryService --> AlertRepo
 AlertHistoryService --> TimingCalculator
 @enduml

