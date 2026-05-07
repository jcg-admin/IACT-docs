.. _uc-rpt-12-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Reporte de Agentes
================================================

.. uml::
 :caption: UC_RPT_12 — flujo de consulta de reporte de agentes.

 @startuml

 start
 :GET con filtros + period;
 :Servicio de Aplicacion verifica autenticacion;
 if (Autenticado?) then (no)
   :401 Unauthorized;
   stop
 endif
 :Verificar capability view_reports;
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
 :Query AgentDailyStat agregado;
 :Calcular KPIs derivados;
 :Construir summary;
 :Cache write;
 :200 OK;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
 - :doc:`diagrama-de-secuencia-detalle`.
 - :doc:`/arquitectura-tecnica/domain-model/agent-report-service`.
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator`.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`.
