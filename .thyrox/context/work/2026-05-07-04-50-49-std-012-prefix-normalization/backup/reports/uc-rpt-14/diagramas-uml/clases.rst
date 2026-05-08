8.3 Clases
==========

.. uml::

 @startuml
 class CampaignReportService
 class CampaignDailyStatRepo
 class KPICalculator
 CampaignReportService --> CampaignDailyStatRepo
 CampaignReportService --> KPICalculator
 @enduml

