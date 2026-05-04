.. _arq-mod-005-diagramas:

================================================
ARQ_MOD_005 — Diagramas de Comportamiento
================================================


Flujo de Acceso a Visualizaciones
===================================

.. uml::
 :caption: Flujo de acceso a visualizaciones — consulta RBAC, segmentos y exportacion.

 @startuml

 start

 :view_reports solicita reporte IVR;

 :JWT + RBAC: verificar view_reports;

 if (Sin permiso?) then (si)
   :403 Forbidden;
   stop
 endif

 :SegmentResolver.resolve(user_id);
 :Mapear DIDs RBAC a segmentos IVR;

 if (Sin segmentos?) then (si)
   :400 USER_WITHOUT_SEGMENT;
   stop
 endif

 :cursor.callproc(sp_rpt_*, [trimestre, segmentos]);

 if (Tiene permiso export_csv?) then (si)
   :Retornar datos + opciones exportacion;
   if (Solicita exportacion?) then (si)
     :Encolar job de exportacion asincrona;
     :Notificar via InternalMailbox;
     stop
   else (no exporta)
     :Retornar dataset al frontend;
   stop
   endif
 else (solo view)
   :Retornar dataset filtrado por segmentos;
   stop
 endif

 @enduml

----

Secuencia sp_rpt_* — Flujo Completo
======================================

.. uml::
 :caption: Secuencia de consulta de reporte IVR via cursor.callproc sobre MariaDB.

 @startuml

 actor "view_reports" as view_reports
 participant "DashboardEndpoint\n(/api/reportes/)" as Dashboardendpoint
 participant "SegmentResolver" as Segmentresolver
 participant "ServicioReportes\n(cursor.callproc)" as Servicioreportes
 database "base_ivr_detalle\nbase_ivr_clientes\n(MariaDB)" as IVRDB

 view_reports -> Dashboardendpoint : GET /api/reportes/?trimestre=Q1
 Dashboardendpoint -> Dashboardendpoint : JWT + RBAC (view_reports)
 Dashboardendpoint -> Segmentresolver : resolve(user_id)
 Segmentresolver -> Segmentresolver : mapear DIDs RBAC a segmentos IVR
 Segmentresolver --> Dashboardendpoint : [nacional_A, nacional_B, Puebla]

 alt sin segmentos
   Dashboardendpoint --> view_reports : 400 USER_WITHOUT_SEGMENT
 else segmentos resueltos
   Dashboardendpoint -> Servicioreportes : callproc(sp_rpt_centros_xsegmento, [Q1])
   Servicioreportes -> IVRDB : CALL sp_rpt_centros_xsegmento(Q1)
   IVRDB --> Servicioreportes : filas por segmento
   Servicioreportes --> Dashboardendpoint : list[dict] filtrada
   Dashboardendpoint --> view_reports : 200 + datos del reporte
 end

 @enduml

----

Diagrama de componentes — MOD_Reports
========================================

.. uml::
 :caption: Componentes de MOD_Reports y sus dependencias de datos.

 @startuml

 component "apps.reports\n(DRF views)" as RPTS
 component "SegmentResolver\n(DID_MAP)" as Segmentresolver
 component "ServicioReportes\n(cursor.callproc)" as Servicioreportes
 component "apps.exports\n(CSV/Excel)" as AppsExports
 component "InternalMailbox" as Internalmailbox

 database "base_ivr_detalle\nbase_ivr_clientes\n(MariaDB — solo lectura)" as base_ivr_detalle
 database "auth_user\naudit_log\n(PostgreSQL)" as auth_user

 RPTS --> Segmentresolver : resolve segmentos
 RPTS --> Servicioreportes : invocar sp_rpt_*
 Servicioreportes --> base_ivr_detalle : CALL sp_rpt_* (lectura)
 RPTS --> auth_user : leer DIDs del usuario (RBAC)
 RPTS --> AppsExports : generar archivo exportado
 AppsExports --> Internalmailbox : notificar disponibilidad

 @enduml
