8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET con period + filtros;
 :JWT + RBAC + segmento;
 :Cache lookup;
 :Query CampaignDailyStat;
 :Calcular conversion rate, calls/hour;
 :Cache write;
 :200;
 stop
 @enduml

