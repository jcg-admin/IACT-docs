8.3 Diagrama de clases
======================

.. uml::
 :caption: Estructura

 @startuml
 class HistoricalReport {
   period
   group_by
   buckets: list[Bucket]
   comparative: Comparative
 }

 class Bucket {
   bucket_key
   kpis: KPISet
 }

 class Comparative {
   period_prior
   kpis_summary
   diff_pct
 }

 HistoricalReport "1" -- "*" Bucket
 HistoricalReport "1" -- "0..1" Comparative
 @enduml

