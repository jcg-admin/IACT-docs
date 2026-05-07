.. _uc-rpt-14-parte-08-diagrama-clases:

8.3 Diagrama de clases
=======================

.. uml::
 :caption: UC_RPT_14 — clases del reporte de campanas.

 @startuml

 class CampaignReportService {
   + list(filters, period) : List
   + detail(campaign_id) : CampaignDetail
 }

 class CampaignDailyStatRepo {
   + aggregate(filters, period) : List
 }

 class KPICalculator {
   + derive_campaign_kpis(stats) : Map
 }

 CampaignReportService --> CampaignDailyStatRepo : reads
 CampaignReportService --> KPICalculator : computes

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`.
