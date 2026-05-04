.. _uc-rpt-16-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_16\nReporte Menus IVR" as UC16
   usecase "Ver menus redirigidos" as VerMenusRedirigidos
   usecase "Ver errores de menu" as VerErroresDeMenu
 }
 view_reports --> UC16
 UC16 ..> INC : <<include>>
 UC16 ..> VerMenusRedirigidos : <<extend>>
 UC16 ..> VerErroresDeMenu : <<extend>>
 @enduml

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

8.3 Distribucion de menus
==========================

.. uml::

 @startuml
 (Entry IVR) --> (Menu principal) : n llamadas
 (Menu principal) --> (Opcion 1 - transferencia) : n
 (Menu principal) --> (cliente_colgo) : n abandono
 (Menu principal) --> (SinOpcion_Cabecera) : n abandono
 (Menu principal) --> (VACIO) : n sin menu
 @enduml

8.4 Clases
==========

.. uml::

 @startuml
 class MenuIVRReportService {
   + get(trimestre, vista, invoker) : ReporteMenuIVR
 }
 class ServicioReportes {
   + menu_redirigidos(trimestre) : list[dict]
   + menu_centro(trimestre) : list[dict]
   + cmenu_error(trimestre) : list[dict]
 }
 class SegmentResolver
 MenuIVRReportService --> ServicioReportes
 MenuIVRReportService --> SegmentResolver
 @enduml
