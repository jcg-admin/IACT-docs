.. _uc-rpt-13-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Reporte de Abandono
=================================================

.. uml::
 :caption: UC_RPT_13 — flujo de consulta de reporte de abandono.

 @startuml

 start
 :GET /api/v1/reportes/abandono/ con trimestre;
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
 :Consultar Servicio de Reportes (sp_rpt_llamadas_abandonadas);
 :Filtrar por segmentos del usuario;
 :Cache write TTL 300s;
 :200 OK con ReporteAbandono;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
 - :doc:`diagrama-de-secuencia`.
 - :doc:`/arquitectura-tecnica/domain-model/abandonment-report-service`.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver`.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache`.
