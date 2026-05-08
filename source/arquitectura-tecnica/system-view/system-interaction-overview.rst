.. meta::
 :artefacto: AT_UML_SISTEMA_08_SECUENCIA
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_secuencia:

====================================
Sistema IACT — Diagrama de Secuencia
====================================

8. Diagrama de Secuencia
=========================

Muestra la interaccion entre el usuario y el Sistema IACT. El
fragmento ``alt`` verifica si hay JWT valido o si es nueva sesion.
El fragmento ``loop`` contiene todos los accesos posibles durante
la sesion. Un fragmento ``neg`` muestra el caso de fallo del ETL
y ``opt`` permite el reintento.

.. uml::
 :caption: Figura 9 — Diagrama de secuencia del Sistema IACT

 @startuml

 actor "view_reports" as view_reports
 participant "AuthEndpoint" as AuthEndpoint
 participant "DashboardEndpoint" as DashboardEndpoint
 participant "SegmentResolver" as SegmentResolver
 participant "ReportingService\n(sp_rpt_*)" as ReportingService
 participant "DisparadorETL" as ProcesoETL
 actor "Sistema IVR\n(fuente)" as SistemaIVR

 alt [autenticacion exitosa: status=TRUE]

   alt [Nueva sesion]
     view_reports -> AuthEndpoint : 1: POST /api/auth/login()
     AuthEndpoint -> AuthEndpoint : 2: ValidarCredenciales()
     AuthEndpoint --> view_reports : 3: status := GenerarJWT(rbac_functions)
   else [JWT valido existente]
     view_reports -> DashboardEndpoint : 4: GET /api/dashboard/ (JWT)
     DashboardEndpoint -> DashboardEndpoint : 5: ValidarJWT_RBAC(view_dashboard)
     DashboardEndpoint --> view_reports : 6: sesion_confirmada
   end

   loop [sesion activa]

     opt [view_dashboard en JWT]
       view_reports -> DashboardEndpoint : 7: GET /api/dashboard/
       DashboardEndpoint -> SegmentResolver : 8: segments_for(user_id)
       SegmentResolver --> DashboardEndpoint : 9: segmentos
       DashboardEndpoint -> ReportingService : 10: callproc(sp_rpt_centros_xsegmento)
       ReportingService --> DashboardEndpoint : 11: KPIs IVR
       DashboardEndpoint --> view_reports : 12: dashboard mostrado
     end

     opt [view_reports en JWT]
       view_reports -> DashboardEndpoint : 13: GET /api/reportes/?trimestre=
       DashboardEndpoint -> SegmentResolver : 14: segments_for(user_id)
       SegmentResolver --> DashboardEndpoint : 15: segmentos
       DashboardEndpoint -> ReportingService : 16: callproc(sp_rpt_*, [trimestre])
       ReportingService --> DashboardEndpoint : 17: rows reporte
       DashboardEndpoint --> view_reports : 18: reporte mostrado
     end

     opt [view_pipeline_status en JWT]
       view_reports -> ETL : 19: POST /api/pipeline/ejecutar/
       ETL -> IVR : 20: leer tbl_historico_*
       ETL -> ETL : 21: CALL sp_etl_maestro(trimestre)
       ETL --> view_reports : 22: estado_ejecucion

       alt [ETL fallido]
         ETL --> view_reports : 23: estado = fallido
         view_reports --> ETL : 24: error en ejecucion
       end

       opt [request_pipeline_retry en JWT]
         par
           view_reports -> ETL : 25: reintentar(trimestre)
           ETL --> view_reports : 26: ejecucion_reintentada
         also
           view_reports -> ETL : 27: cancelar_reintento()
           ETL --> view_reports : 28: reintento_cancelado
         end
       end
     end

   end

 else [autenticacion fallida: status=FALSE]
   view_reports -> AuthEndpoint : 29: login_fallido()
   AuthEndpoint -->x view_reports : 30: <<destroy>> 401 Unauthorized
 end

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
