8.3 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_RPT_01 — secuencia

 @startuml

 actor "User" as User
 participant "Frontend" as Frontend
 participant "DashboardEndpoint" as Dashboardendpoint
 participant "SegmentResolver" as Segmentresolver
 participant "MetricsCache" as Metricscache
 participant "ReportingService\n(sp_rpt_*)" as Servicioreportes
 database "BD_IVR" as BdIvrLegacy

 User -> Frontend: abrir dashboard
 Frontend -> Dashboardendpoint: GET /api/dashboard/
 Dashboardendpoint -> Dashboardendpoint: JWT + RBAC
 Dashboardendpoint -> Segmentresolver: segments_for(user_id)
 Segmentresolver --> Dashboardendpoint: segments
 Dashboardendpoint -> Metricscache: get(key)
 Metricscache --> Dashboardendpoint: miss
 Dashboardendpoint -> Servicioreportes: cursor.callproc(sp_rpt_centros_xsegmento, [period, segments])
 Servicioreportes -> BdIvrLegacy: CALL sp_rpt_centros_xsegmento
 BdIvrLegacy --> Servicioreportes: filas pre-agregadas
 Servicioreportes --> Dashboardendpoint: rows (kpis + trend ya calculados)
 Dashboardendpoint -> Metricscache: set(key, response, ttl=30)
 Dashboardendpoint --> Frontend: 200 + dashboard
 Frontend --> User: render

 loop cada 30s
   Frontend -> Dashboardendpoint: GET /api/dashboard/
   Dashboardendpoint -> Metricscache: get
   Metricscache --> Dashboardendpoint: hit
   Dashboardendpoint --> Frontend: cached
 end

 @enduml

