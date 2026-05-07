.. _uc-rpt-16-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Reporte de Menus IVR
==================================================

.. uml::
 :caption: UC_RPT_16 — flujo de consulta de reporte de menus IVR.

 @startuml

 start
 :GET /api/v1/reportes/menus-ivr/ con trimestre y vista;
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
 if (vista = redirigidos) then
   :Consultar sp_rpt_menu_redirigidos;
 elseif (vista = menu_centro) then
   :Consultar sp_rpt_menu_centro;
 else
   :Consultar sp_rpt_cMENU_ERROR;
 endif
 :Filtrar por segmentos del usuario;
 :Cache write TTL 300s;
 :200 OK con ReporteMenuIVR;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`diagrama-de-clases`.
 - :doc:`diagrama-de-distribucion-de-menus`.
