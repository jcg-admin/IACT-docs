.. meta::
 :artefacto: ARQ_MOD_005_DIAG_SECUENCIA_SPT
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/vis-reports/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_005_secuencia_sp_rpt_flujo:

===================================
Secuencia sp_rpt_* — Flujo Completo
===================================

.. uml::
 :caption: Secuencia de consulta de reporte IVR via cursor.callproc sobre Almacen de Datos.

 @startuml

 actor "view_reports" as view_reports
 participant "DashboardEndpoint\n(/api/reportes/)" as Dashboardendpoint
 participant "SegmentResolver" as Segmentresolver
 participant "ServicioReportes\n(cursor.callproc)" as Servicioreportes
 database "base_ivr_detalle\nbase_ivr_clientes" as BD_IVR

 view_reports -> Dashboardendpoint : GET /api/reportes/?trimestre=Q1
 Dashboardendpoint -> Dashboardendpoint : JWT + RBAC (view_reports)
 Dashboardendpoint -> Segmentresolver : resolve(user_id)
 Segmentresolver -> Segmentresolver : mapear DIDs RBAC a segmentos IVR
 Segmentresolver --> Dashboardendpoint : [nacional_A, nacional_B, Puebla]

 alt sin segmentos
   Dashboardendpoint --> view_reports : 400 USER_WITHOUT_SEGMENT
 else segmentos resueltos
   Dashboardendpoint -> Servicioreportes : callproc(sp_rpt_centros_xsegmento, [Q1])
   Servicioreportes -> BD_IVR : CALL sp_rpt_centros_xsegmento(Q1)
   BD_IVR --> Servicioreportes : filas por segmento
   Servicioreportes --> Dashboardendpoint : list[dict] filtrada
   Dashboardendpoint --> view_reports : 200 + datos del reporte
 end

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/vis-reports/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
