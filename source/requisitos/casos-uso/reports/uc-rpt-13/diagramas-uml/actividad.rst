8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/reportes/abandono/?trimestre=;
 :JWT + RBAC (view_reports);
 :Resolver segmento (<<include>> UC_INC_RPT_01);
 :Cache lookup;
 :Consultar Servicio de Reportes (sp_rpt_llamadas_abandonadas);
 :Filtrar por segmentos del usuario;
 :Cache write TTL 300s;
 :200 con ReporteAbandono;
 stop
 @enduml

