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
 participant "ServicioReportes\n(sp_rpt_*)" as Servicioreportes
 participant "KPICalculator" as Kpicalculator

 User -> Frontend: abrir dashboard
 Frontend -> Dashboardendpoint: GET /api/dashboard/
 Dashboardendpoint -> Dashboardendpoint: JWT + RBAC
 Dashboardendpoint -> Segmentresolver: segments_for(user_id)
 Segmentresolver --> Dashboardendpoint: segments
 Dashboardendpoint -> Metricscache: get(key)
 Metricscache --> Dashboardendpoint: miss
 Dashboardendpoint -> Servicioreportes: cursor.callproc(sp_rpt_centros_xsegmento, [trimestre])
 Servicioreportes --> Dashboardendpoint: rows agregados
 Dashboardendpoint -> Kpicalculator: derive_kpis(rows)
 Kpicalculator --> Dashboardendpoint: kpis
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

