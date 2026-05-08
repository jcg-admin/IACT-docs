.. _uc-alr-04-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_ALR_04 — clases involucradas en consulta historica.

 @startuml

 class AlertHistoryService {
   + query(filters, period) : AlertHistorySummary
 }

 class AlertRepo {
   + query_history(filters, period) : List
 }

 class TimingCalculator {
   + compute_ttak(rows) : Duration
   + compute_ttar(rows) : Duration
 }

 class AlertHistorySummary {
   + total_alerts : Integer
   + by_severity : Map
   + ttak_p50 : Duration
   + ttar_p50 : Duration
   + rows : List
 }

 AlertHistoryService --> AlertRepo : reads
 AlertHistoryService --> TimingCalculator : computes
 AlertHistoryService --> AlertHistorySummary : returns

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator`.
