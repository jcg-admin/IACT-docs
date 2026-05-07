.. _uc-rpt-14-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Reporte de Campanas
==================================================

.. uml::
 :caption: UC_RPT_14 — flujo de consulta de reporte de campanas.

 @startuml

 start
 :GET con period y filtros;
 :Servicio de Aplicacion verifica capability view_reports;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif
 :Resolver segmento (UC_INC_RPT_01);
 :Cache lookup;
 if (Cache HIT?) then (si)
   :Return cached;
   stop
 endif
 :Query CampaignDailyStat;
 :Calcular conversion rate y calls/hour;
 :Cache write;
 :200 OK con datos de campanas;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
 - :doc:`diagrama-de-secuencia`.
