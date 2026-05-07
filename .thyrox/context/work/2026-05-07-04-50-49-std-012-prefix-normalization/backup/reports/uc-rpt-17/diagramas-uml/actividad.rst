8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/reportes/clientes/?trimestre=;
 :JWT + RBAC (view_reports);
 :Resolver segmento (<<include>> UC_INC_RPT_01);
 :Cache lookup;
 :Consultar Servicio de Reportes (sp_rpt_clientes);
 :Filtrar por segmentos del usuario;
 :Cache write TTL 300s;
 :200 con ReporteClientes (telefono_hashed);
 stop
 @enduml

