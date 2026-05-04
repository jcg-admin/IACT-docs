.. _uc-rpt-13-parte-08:

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
   usecase "UC_RPT_13\nReporte Abandono" as UC13
 }
 view_reports --> UC13
 UC13 ..> INC : <<include>>
 @enduml

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

8.3 Clases
==========

.. uml::

 @startuml
 class AbandonoReportService {
   + get(trimestre, invoker) : ReporteAbandono
 }
 class ServicioReportes {
   + llamadas_abandonadas(trimestre) : list[dict]
 }
 class SegmentResolver {
   + resolve(user_id) : list[str]
 }
 AbandonoReportService --> ServicioReportes
 AbandonoReportService --> SegmentResolver
 @enduml

8.4 Secuencia
=============

.. uml::

 @startuml
 actor "view_reports" as view_reports
 participant "View" as View
 participant "SegmentResolver" as Segmentresolver
 database "Base Analitica IVR\n(sp_rpt_llamadas_abandonadas)" as BaseAnaliticaIvr
 view_reports -> View: GET /reportes/abandono/
 View -> View: JWT + RBAC
 View -> Segmentresolver: resolve(user_id)
 Segmentresolver --> View: [nacional_A, ...]
 View -> BaseAnaliticaIvr: cursor.callproc(sp_rpt_llamadas_abandonadas, [trimestre])
 BaseAnaliticaIvr --> View: rows abandono por segmento
 View --> view_reports: 200 ReporteAbandono
 @enduml
