8.2 Actividad
=============

.. uml::

 @startuml
 start
 :GET /api/v1/reportes/menus-ivr/?trimestre=&vista=;
 :JWT + RBAC (view_reports);
 :Resolver segmento (<<include>> UC_INC_RPT_01);
 :Cache lookup;
 if (vista = 'redirigidos') then
   :Consultar sp_rpt_menu_redirigidos;
 elseif (vista = 'menu_centro') then
   :Consultar sp_rpt_menu_centro;
 else
   :Consultar sp_rpt_cMENU_ERROR;
 endif
 :Filtrar por segmentos del usuario;
 :Cache write TTL 300s;
 :200 con ReporteMenuIVR;
 stop
 @enduml

