.. _uc-rpt-13-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
 left to right direction
 actor "Supervisor\nde Operaciones" as USR
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_13\nReporte Abandono" as UC13
 }
 USR --> UC13
 UC13 ..> INC : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 !include ../../_static/plantuml-styles.puml
 start
 :GET /api/v1/reportes/abandono/?trimestre=;
 :JWT + RBAC (view_queue_reports);
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
 !include ../../_static/plantuml-styles.puml
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
 !include ../../_static/plantuml-styles.puml
 actor "Supervisor" as U
 participant "View" as V
 participant "SegmentResolver" as SR
 database "Base Analitica IVR\n(sp_rpt_llamadas_abandonadas)" as DB
 U -> V: GET /reportes/abandono/
 V -> V: JWT + RBAC
 V -> SR: resolve(user_id)
 SR --> V: [nacional_A, ...]
 V -> DB: cursor.callproc(sp_rpt_llamadas_abandonadas, [trimestre])
 DB --> V: rows abandono por segmento
 V --> U: 200 ReporteAbandono
 @enduml
