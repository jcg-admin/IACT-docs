.. meta::
 :artefacto: AT_UML_SISTEMA_09_COMUNICACION
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_comunicacion:

=======================================
Sistema IACT — Diagrama de Comunicacion
=======================================

9. Diagrama de Comunicacion
=============================

Focaliza en la interaccion entre los objetos del sistema. Los
mensajes numerados representan los condicionales e iteraciones.
Los mensajes con ``*`` indican iteracion; con ``[condicion]``
indican guarda basada en funcion RBAC del JWT activo.

.. uml::
 :caption: Figura 10 — Diagrama de comunicacion del Sistema IACT

 @startuml

 object ": User (RBAC group)" as UserRBAC
 object ": AuthEndpoint" as AuthEndpoint
 object ": DashboardEndpoint" as DashboardEndpoint
 object ": SegmentResolver" as SegmentResolver
 object ": ServicioReportes" as ServicioReportes
 object ": DisparadorETL" as ProcesoETL
 object "AutenticacionFallida" as AutenticacionFallida

 UserRBAC --> AuthEndpoint : 1: check_credentials()
 AuthEndpoint --> AuthEndpoint : 2: status := ValidarJWT(rbac_functions)
 AuthEndpoint --> UserRBAC : 3: [status==TRUE] GenerarJWT()
 AuthEndpoint --> DashboardEndpoint : 4 *[status==TRUE]: dashboard_data()
 DashboardEndpoint --> SegmentResolver : 5 *[view_dashboard]: segments_for(user_id)
 SegmentResolver --> DashboardEndpoint : 6: segmentos
 DashboardEndpoint --> ServicioReportes : 7 *[view_dashboard]: callproc(sp_rpt_centros_xsegmento)
 ServicioReportes --> DashboardEndpoint : 8: KPIs IVR
 DashboardEndpoint --> UserRBAC : 9: dashboard_mostrado
 UserRBAC --> DashboardEndpoint : 10 *[view_reports]: reporte(trimestre)
 DashboardEndpoint --> ServicioReportes : 11 *[view_reports]: callproc(sp_rpt_*)
 ServicioReportes --> DashboardEndpoint : 12: rows_reporte
 DashboardEndpoint --> UserRBAC : 13: reporte_mostrado
 UserRBAC --> ETL : 14 *[view_pipeline_status]: disparar_etl(trimestre)
 ETL --> ETL : 15: CALL sp_etl_maestro(trimestre)
 ETL --> UserRBAC : 16: estado_ejecucion
 UserRBAC --> ETL : 17 *[request_pipeline_retry]: request_pipeline_retry()
 ETL --> UserRBAC : 18 *[success==TRUE]: ejecucion_reintentada
 ETL --> UserRBAC : 19: receiptStatus := cancelar_reintento
 UserRBAC --> AuthEndpoint : 20 *[status==FALSE]: AutenticacionFallida() <<destroy>>
 AutenticacionFallida --> UserRBAC : 21 *[status==FALSE]: AutenticacionFallida()

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
