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
