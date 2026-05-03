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
   :403 Forbidden; stop
 endif

 :SegmentResolver.resolve(user_id);
 :Mapear DIDs RBAC a segmentos IVR;

 if (Sin segmentos?) then (si)
   :400 USER_WITHOUT_SEGMENT; stop
 endif

 :cursor.callproc(sp_rpt_*, [trimestre, segmentos]);

 if (Tiene permiso export_csv?) then (si)
   :Retornar datos + opciones exportacion;
   if (Solicita exportacion?) then (si)
     :Encolar job de exportacion asincrona;
     :Notificar via InternalMailbox;
     stop
   else (no exporta)
     :Retornar dataset al frontend; stop
   endif
 else (solo view)
   :Retornar dataset filtrado por segmentos; stop
 endif

 @enduml

----

Secuencia sp_rpt_* — Flujo Completo
======================================

.. uml::
 :caption: Secuencia de consulta de reporte IVR via cursor.callproc sobre MariaDB.

 @startuml

 actor "view_reports" as U
 participant "DashboardEndpoint\n(/api/reportes/)" as EP
 participant "SegmentResolver" as SR
 participant "ServicioReportes\n(cursor.callproc)" as SVC
 database "base_ivr_detalle\nbase_ivr_clientes\n(MariaDB)" as IVRDB

 U -> EP : GET /api/reportes/?trimestre=Q1
 EP -> EP : JWT + RBAC (view_reports)
 EP -> SR : resolve(user_id)
 SR -> SR : mapear DIDs RBAC a segmentos IVR
 SR --> EP : [nacional_A, nacional_B, Puebla]

 alt sin segmentos
   EP --> U : 400 USER_WITHOUT_SEGMENT
 else segmentos resueltos
   EP -> SVC : callproc(sp_rpt_centros_xsegmento, [Q1])
   SVC -> IVRDB : CALL sp_rpt_centros_xsegmento(Q1)
   IVRDB --> SVC : filas por segmento
   SVC --> EP : list[dict] filtrada
   EP --> U : 200 + datos del reporte
 end

 @enduml

----

Diagrama de componentes — MOD_Reports
========================================

.. uml::
 :caption: Componentes de MOD_Reports y sus dependencias de datos.

 @startuml

 component "apps.reports\n(DRF views)" as RPTS
 component "SegmentResolver\n(DID_MAP)" as SR
 component "ServicioReportes\n(cursor.callproc)" as SVC
 component "apps.exports\n(CSV/Excel)" as EXP
 component "InternalMailbox" as MB

 database "base_ivr_detalle\nbase_ivr_clientes\n(MariaDB — solo lectura)" as IVR
 database "auth_user\naudit_log\n(PostgreSQL)" as PG

 RPTS --> SR : resolve segmentos
 RPTS --> SVC : invocar sp_rpt_*
 SVC --> IVR : CALL sp_rpt_* (lectura)
 RPTS --> PG : leer DIDs del usuario (RBAC)
 RPTS --> EXP : generar archivo exportado
 EXP --> MB : notificar disponibilidad

 @enduml
