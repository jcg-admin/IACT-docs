.. _uc-rpt-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_01 — dashboard

 @startuml
 left to right direction

 actor "User con funcion\nview_reports" as USR
 actor "Frontend" as FE

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC
   usecase "UC_RPT_01\nVer Dashboard IVR" as UC01
   usecase "Auto-refresh" as REF
 }

 USR --> FE
 FE --> UC01
 UC01 ..> INC : <<include>>
 UC01 ..> REF : <<extend>>

 note bottom of UC01
   Read-only Analytics (CNST-007).
   Sin auditoria por invocacion.
 end note

 @enduml

8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_RPT_01 — flujo

 @startuml

 start
 :GET /api/dashboard/?period=today;
 if (JWT?) then (no)
   :401; stop
 endif
 if (view_reports?) then (no)
   :403 + audit; stop
 endif
 :Resolver segmentos del User;
 if (Sin segmentos?) then (si)
   :400 USER_WITHOUT_SEGMENT; stop
 else (no)
 endif
 :Validar periodo;
 if (Cache hit?) then (si)
   :return cached;
   stop
 else (no)
 endif
 :Consultar Servicio de Reportes (sp_rpt_centros_xsegmento);
 :Calcular derivados (TMO, SL, abandono);
 :Construir response;
 :Cache write;
 :200 OK;
 stop

 @enduml

8.3 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_RPT_01 — secuencia

 @startuml

 actor "User" as U
 participant "Frontend" as FE
 participant "DashboardEndpoint" as DE
 participant "SegmentResolver" as SR
 participant "MetricsCache" as MC
 participant "ServicioReportes\n(sp_rpt_*)" as AR
 participant "KPICalculator" as KC

 U -> FE: abrir dashboard
 FE -> DE: GET /api/dashboard/
 DE -> DE: JWT + RBAC
 DE -> SR: segments_for(user_id)
 SR --> DE: segments
 DE -> MC: get(key)
 MC --> DE: miss
 DE -> AR: cursor.callproc(sp_rpt_centros_xsegmento, [trimestre])
 AR --> DE: rows agregados
 DE -> KC: derive_kpis(rows)
 KC --> DE: kpis
 DE -> MC: set(key, response, ttl=30)
 DE --> FE: 200 + dashboard
 FE --> U: render

 loop cada 30s
   FE -> DE: GET /api/dashboard/
   DE -> MC: get
   MC --> DE: hit
   DE --> FE: cached
 end

 @enduml

8.4 Diagrama de estado del trend
================================

.. uml::
 :caption: Estado de carga del trend

 @startuml
 [*] --> Empty
 Empty --> Loading : query
 Loading --> Loaded : rows OK
 Loading --> Stale : ETL atrasado
 Loading --> Error : timeout
 Loaded --> Empty : period change
 Stale --> Loaded : ETL recuperado
 Error --> Loading : retry
 @enduml
